""" Twitter Handler """
import json
import logging
import re
import unidecode
import twitter


class TwitterHandler():
    """Class to interface with Twitter"""
    # '#' must be replaced by '%23' for http?
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
            # Convert characters to ASCII
            text = unidecode.unidecode(text)
            # text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')

            sl[i]["Text"] = text

        return sl

    def post_reply(self, message, uid):
        """Post reply tweet to specified message"""
        logging.info("Tweeting message <%s>" % message)
        self.api.PostUpdate(message)

    def post_video_reply(self, message, uid, video_file):
        """Upload video to Twitter and post as a reply to tweet with 'id'"""
        # Upload the video file first
        with open(video_file, "rb") as f:
            # media_id = self.api.UploadMediaChunked(f)
            logging.info("Posting video update..")
            status = self.api.PostUpdate("Here is your reply", media=f,
                                         in_reply_to_status_id=uid)

        return status
