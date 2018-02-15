""" Twitter Handler """
import json
import logging
import re
import unidecode
import twitter
import threading
import time

logger = logging.getLogger(__name__)

class TwitterHandler():
    """Class to interface with Twitter"""
    hashtag = "#sevensegsay"
    token_file = "auth.json"

    def __init__(self):
        """Initializer"""
        logger.debug("Reading twitter auth data from <%s>" % self.token_file)
        with open(self.token_file, "r") as f:
            json_data = json.load(f)

        logger.info("logger into Twitter..")
        self.api = twitter.Api(consumer_key=json_data["consumer_key"],
                               consumer_secret=json_data["consumer_secret"],
                               access_token_key=json_data["access_token_key"],
                               access_token_secret=json_data["access_token_secret"])

    def post_reply(self, message, tweet, video_file=None):
        """Upload message to Twitter. Handles video as well"""
        message = str(message) + " @%s" %tweet["ScreenName"]
        logger.info("Tweeting message <%s>" % message)
        if video_file is None:
            logger.debug("Posting standard tweet..")
            status = self.api.PostUpdate(message, in_reply_to_status_id=tweet["ID"])
        else:
            with open(video_file, "rb") as f:
                logger.debug("Posting video update..")
                status = self.api.PostUpdate(message, media=f,
                                             in_reply_to_status_id=tweet["ID"])

    def start_stream(self, queue):
        logger.debug("Initializing Twitter streamer thread")
        thread = TwitterStreamerThread(self.api, self.hashtag, queue)
        thread.daemon = True
        logger.debug("Launching Twitter streamer thread")
        thread.start()
        return thread

    def start_old_message_scrubber(self, queue, interval=60):
        thread = TwitterOldMessageScrubber(self.api, self.hashtag, queue, interval)
        thread.daemon = True
        thread.start()
        return thread


class TwitterStreamerThread(threading.Thread):
    """A thread for streaming data from Twitter and putting it into a queue"""
    def __init__(self, api, hashtag, queue, name="TwitterStreamerThread"):
        super().__init__()
        self.api = api
        self.queue = queue
        self.hashtag = hashtag

    def run(self):
        logger.debug("Initialized Twitter Stream. Looking for: %s" %(self.hashtag))
        stream = self.api.GetStreamFilter(track=[self.hashtag])
        # stream = self.api.GetStreamSample()

        for s in stream:
            if "text" in s:
                logger.info("STREAMER: Got a Tweet:\t%s" %s["text"])
                self.queue.put({"ID": s["id"], "ScreenName": s["user"]["screen_name"],
                                    "Text": _clean_up_text(s["text"], self.hashtag)})

        debug.critical("Streamer thread terminated")


class TwitterOldMessageScrubber(threading.Thread):
    """Thread that periodically polls REST API for old messages that are not displayed"""
    def __init__(self, api, hashtag, queue, interval, name="TwitterOldMessageScrubber"):
        super().__init__()
        self.api = api
        self.queue = queue
        self.hashtag = hashtag
        self.interval = interval

    def run(self):
        """Search for Tweets containing the hashtag in history

        This uses the REST API search/tweets.json call. It searcehes past 7 days
        in the free API version and is not guaranteed to return all the results.
        """
        logger.debug("Initialized REST API scrubber thread")

        while(True):
            query = self.api.GetSearch(term=[self.hashtag])
            # Filter out only status updates
            hashtag_statuses = [s for s in query if type(s) == twitter.Status]
            logger.debug("Running Scrubber. Got %d old tweet(s):" %(len(hashtag_statuses)))
            for h in hashtag_statuses:
                logger.debug("Tweet = ", h.text)

            # Retreive current user's most recent tweets. 200 is max allowed
            query = self.api.GetUserTimeline(count=200)
            user_statuses = [s for s in query if type(s) == twitter.Status]
            logger.debug("Got %d recent status(es) from the current user"
                          %(len(user_statuses)))

            replied_ids = []
            for s in user_statuses:
                if s.in_reply_to_status_id is not None:
                    # We already have replied something
                    replied_ids.append(s.in_reply_to_status_id)

            logger.debug("Out of %d user statuses %d were our own replies to some tweets"
                          %(len(user_statuses), len(replied_ids)))

            status_list = []
            for s in hashtag_statuses:
                if s.id not in replied_ids:
                    tweet_dict = {"ID": s.id, "ScreenName": s.user.screen_name,
                                        "Text": _clean_up_text(s.text, self.hashtag)}
                    print(tweet_dict)
                    for k in tweet_dict:
                        print(type(k), k)
                    status_list.append(tweet_dict)

            msg_counter = 0
            for s in status_list:
                if s in self.queue.queue:
                    logger.debug("Message already in queue")
                else:
                    logger.debug("Putting message into queue")
                    self.queue.put(s)
                    msg_counter += 1

            logger.info("Got %d messages, that need replies." %(msg_counter))

            time.sleep(self.interval)

        debug.critical("Old message scrubber terminated")

def _clean_up_text(text, hashtag):
    """Get tweeted messages, strip hashtags and convert characters to ascii"""
    pattern = re.compile(re.escape(hashtag), re.IGNORECASE)
    # Get rid of hashtag (Case insensitive)
    text = pattern.sub("", text)
    # Trim leading and ending whitespaces
    text = text.lstrip()
    text = text.rstrip()
    # Convert unicode to standard characters
    text = unidecode.unidecode(text)

    return text
