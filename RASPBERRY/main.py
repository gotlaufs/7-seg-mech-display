#!/usr/bin/env python3
""" Main Parrot app """

import time
import logging
import subprocess
import traceback
import sys
import select
import queue
import os

if os.uname()[4].startswith("arm"):
    import picamera
    import arduino_handler
else:
    import mock.picamera as picamera
    import mock.arduino_handler as arduino_handler

import twitter_handler

# This should work on Raspberry, but just in case adjust as neccessary
ARDUINO_PORT = "/dev/ttyUSB0"

# Pause between main loop iterations
LOOP_DELAY = 15

# If True, will print the whole Python traceback on every handled exception
PRINT_FULL_EXCEPTION = True

# Should not me changed
VIDEO_FILE = "video.h264"
VIDEO_FILE2 = "video.mp4"
# Use ffmpeg to put raw h.264 video in mp4 container with no re-encodeing
# 'y' to all questions
ENCODE_CMD = ["ffmpeg", "-loglevel", "24", "-y", "-i", VIDEO_FILE, "-c", "copy", VIDEO_FILE2]

class TwitterParrot():
    """Twitter Parrot App"""

    def __init__(self):
        logging.info("Starting script")

        logging.info("Initializing Arduino communication")
        self.arduino = arduino_handler.ArduinoHandler(ARDUINO_PORT)
        logging.info("Setting Arduino display parameters")
        self.arduino.blank(False)
        self.arduino.letter_delay(100)
        self.arduino.word_delay(200)

        logging.info("Initializing camera")
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1280, 720)

        logging.info("Initializing Twitter")
        self.tw = twitter_handler.TwitterHandler()

    def show_tweet(self, tweet):
        """Show a single Tweet, record it and post a reply"""
        logging.info("Displaying message: %s" % tweet["Text"])
        logging.info("Starting video recording")
        time_start = time.time()
        # TODO: Add exception handling here
        self.camera.start_recording(VIDEO_FILE, format="h264", quality=23)
        try:
            self.arduino.say(tweet["Text"])
        except Exception as exc:
            # TODO: Log error
            if PRINT_FULL_EXCEPTION:
                print(traceback.format_exc())
            print(exc)

            logging.error("Fail in Arduino comm.")
            return False

        logging.debug("Stopping recording")
        self.camera.stop_recording()
        time_stop = time.time()

        # Add some random scaling factor, because videos turn out to be longer than Python timing
        time_video = (time_stop - time_start) * 1.206
        try:
            logging.info("Recording length is %d seconds" % time_video)
        except FileNotFoundError:
            logging.critical("'ffmpeg' not installed! Exiting..")
            sys.exit()

        if time_video < 30:

            # Put raw video into MP4 container
            logging.info("Calling ffmpeg..")
            # Capture output, so it doesn't clog the screen
            p = subprocess.run(ENCODE_CMD, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
            if p.returncode == 0:
                logging.info("Video conversion done")
            else:
                # TODO: Add stderr and stdout to logging in case of error
                logging.error("ffmpeg failed with code: %d" % p.returncode)
                logging.debug(p.stderr)
                return False

            # Post the video to Twitter
            m = self.get_reply_message()
            try:
                self.tw.post_video_reply(message=m, uid=tweet["ID"],
                                    video_file=VIDEO_FILE2)
            except Exception as exc:
                # TODO: Log exception, not just print
                if PRINT_FULL_EXCEPTION:
                    print(traceback.format_exc())
                print(exc)

                logging.error("Some error while posting Twitter video")
                return False

            logging.info("Succesfully posted video tweet")
            return True

        else:
            logging.error("Recording too long! Discarding..")

            message = ("Unfortunately Twitter only allows 30s video. "
                       "Your message was %ds :(" % time_video)
            try:
                tw.post_reply(message, tweet["ID"])
            except Exception as exc:
                # TODO: Log exception, not just print
                if PRINT_FULL_EXCEPTION:
                    print(traceback.format_exc())
                print(exc)

                logging.error("Some error while posting a regular Tweet")
                return False

            logging.info("Succesfully posted a reply tweet")
            return True

    def get_reply_message(self):
        """Return a text message that is attached to the reply video"""
        # TODO: Make this something interesting
        return "You say and I reply :)"

    def run(self):
        """Main program loop"""
        # TODO: Restart Streaming interface on errors?
        # TODO: Run search API periodically. Another thread?
        q = queue.Queue();
        try:
            tweet_list = self.tw.get_old_messages()
        except Exception as exc:
            # TODO: Log exceptions
            if PRINT_FULL_EXCEPTION:
                print(traceback.format_exc())
            print(exc)

            logging.error("Exception while getting tweets! API rate limiting?")
            return

        logging.info("Got %d tweets from Search API that need displaying" % len(tweet_list))

        for tweet in tweet_list:
            q.put(tweet)

        # Launch Twitter Streaming thread
        self.tw.start_stream(q)

        # Main Loop
        while(True):
            logging.debug("There are %d items in the queue" %(q.qsize()))
            if q.empty():
                time.sleep(10)
            else:
                tweet = q.get()

            retcode = self.show_tweet(tweet)
            if not retcode:
                logging.warning("Putting tweet back into queue due to errors")
                q.put(tweet)
                time.sleep(10)

        self.arduino.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = TwitterParrot()
    app.run()
