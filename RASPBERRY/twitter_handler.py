""" Twitter Handler """
import json
import logging
import re
import unidecode
import twitter
import threading
import time

class TwitterHandler():
    """Class to interface with Twitter"""
    hashtag = "#sevensegsay"
    token_file = "auth.json"

    def __init__(self):
        """Initializer"""
        logging.debug("Reading twitter auth data from <%s>" % self.token_file)
        with open(self.token_file, "r") as f:
            json_data = json.load(f)

        logging.info("Logging into Twitter..")
        self.api = twitter.Api(consumer_key=json_data["consumer_key"],
                               consumer_secret=json_data["consumer_secret"],
                               access_token_key=json_data["access_token_key"],
                               access_token_secret=json_data["access_token_secret"])

    def get_messages_dict(self):
        """Find the Tweets with the hashtag"""
        # '#' must be replaced by '%23' for http?
        hashtag = self.hashtag.replace("#", "%23")
        query = self.api.GetSearch(term=self.hashtag)

        # Filter out only status updates
        statuses = [s for s in query if type(s) == twitter.Status]

        # Convert to dict for easy JSON storage
        status_list = []
        for s in statuses:
            status_list.append({"ID": s.id, "ScreenName": s.user.screen_name,
                               "Text": s.text})

        return status_list

    def get_messages_clean(self):
        """Get tweeted messages, strip hashtags and convert characters to ascii"""
        pattern = re.compile(re.escape(self.hashtag), re.IGNORECASE)
        sl = self.get_messages_dict()
        for i, s in enumerate(sl):
            text = sl[i]["Text"]
            # Get rid of hashtag (Case insensitive)
            text = pattern.sub("", text)
            # Trim leading and ending whitespaces
            text = text.lstrip()
            text = text.rstrip()
            # Convert unicode to standard characters
            text = unidecode.unidecode(text)

            sl[i]["Text"] = text

        return sl

    def post_reply(self, message, uid):
        """Post reply tweet to specified message"""
        logging.info("Tweeting message <%s>" % message)
        status = self.api.PostUpdate(message, in_reply_to_status_id=uid)

        return status

    def post_video_reply(self, message, uid, video_file):
        """Upload video to Twitter and post as a reply to tweet with 'uid'"""
        # Upload the video file first
        with open(video_file, "rb") as f:
            # media_id = self.api.UploadMediaChunked(f)
            logging.info("Posting video update..")
            status = self.api.PostUpdate("Here is your reply", media=f,
                                         in_reply_to_status_id=uid)

        return status

    def get_old_messages(self):
        """Search for Tweets containing the hashtag in history

        This uses the REST API search/tweets.json call. It searcehes past 7 days
        in the free API version and is not guaranteed to return all the results.
        """
        query = self.api.GetSearch(term=[self.hashtag])
        # Filter out only status updates
        hashtag_statuses = [s for s in query if type(s) == twitter.Status]
        logging.debug("Got %d old tweet(s)" %(len(hashtag_statuses)))

        # Retreive current user's most recent tweets. 200 is max allowed
        query = self.api.GetUserTimeline(count=200)
        user_statuses = [s for s in query if type(s) == twitter.Status]
        logging.debug("Got %d recent status(es) from the current user"
                      %(len(user_statuses)))

        replied_ids = []
        for s in user_statuses:
            if s.in_reply_to_status_id is not None:
                # We already have replied something
                replied_ids.append(s.id)

        logging.debug("Out of %d user statuses %d were our own replies"
                      %(len(user_statuses), len(replied_ids)))

        status_list = []
        for s in hashtag_statuses:
            if s.id not in replied_ids:
                status_list.append({"ID": s.id, "ScreenName": s.user.screen_name,
                                    "Text": _clean_up_text(s.text, self.hashtag)})

        logging.info("Got %d messages, that need replies" %(len(status_list)))
        return status_list

    def start_stream(self, queue):
        logging.debug("Initializing Twitter streamer thread")
        thread = TwitterStreamerThread(self.api, self.hashtag, queue)
        thread.daemon = True
        logging.debug("Launching Twitter streamer thread")
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
        logging.debug("Initialized Twitter Stream. Looking for: %s" %(self.hashtag))
        stream = self.api.GetStreamFilter(track=[self.hashtag])
        # stream = self.api.GetStreamSample()

        for s in stream:
            if "text" in s:
                logging.info("Got a Tweet:\t%s" %s["text"])
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
        logging.debug("Initialized REST API scrubber thread")

        while(True):
            query = self.api.GetSearch(term=[self.hashtag])
            # Filter out only status updates
            hashtag_statuses = [s for s in query if type(s) == twitter.Status]
            logging.debug("Got %d old tweet(s)" %(len(hashtag_statuses)))

            # Retreive current user's most recent tweets. 200 is max allowed
            query = self.api.GetUserTimeline(count=200)
            user_statuses = [s for s in query if type(s) == twitter.Status]
            logging.debug("Got %d recent status(es) from the current user"
                          %(len(user_statuses)))

            replied_ids = []
            for s in user_statuses:
                if s.in_reply_to_status_id is not None:
                    # We already have replied something
                    replied_ids.append(s.id)

            logging.debug("Out of %d user statuses %d were our own replies"
                          %(len(user_statuses), len(replied_ids)))

            status_list = []
            for s in hashtag_statuses:
                if s.id not in replied_ids:
                    status_list.append({"ID": s.id, "ScreenName": s.user.screen_name,
                                        "Text": _clean_up_text(s.text, self.hashtag)})

            msg_counter = 0
            for s in status_list:
                if s in self.queue.queue:
                    logging.debug("Message already in queue")
                else:
                    logging.debug("Putting message into queue")
                    self.queue.put(s)
                    msg_counter += 1

            logging.info("Got %d messages, that need replies." %(msg_counter))

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
