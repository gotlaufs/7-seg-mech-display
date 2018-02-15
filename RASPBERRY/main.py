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

logger = logging.getLogger("MAIN")

# This should work on Raspberry, but just in case adjust as neccessary
ARDUINO_PORT = "/dev/ttyUSB0"

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
        logger.info("Starting script")

        logger.info("Initializing Arduino communication")
        self.arduino = arduino_handler.ArduinoHandler(ARDUINO_PORT)
        logger.info("Setting Arduino display parameters")
        self.arduino.blank(False)
        self.arduino.letter_delay(100)
        self.arduino.word_delay(200)

        logger.info("Initializing Twitter")
        self.tw = twitter_handler.TwitterHandler()

    def show_tweet(self, tweet):
        """Show a single Tweet, record it and post a reply"""
        logger.info("Displaying message: %s" % tweet["Text"])
        logger.info("Starting video recording")
        time_start = time.time()
        # TODO: Add exception handling here. Maybe
        try:
            logger.info("Initializing camera")
            self.camera = picamera.PiCamera()
            self.camera.resolution = (1280, 720)
            self.camera.start_recording(VIDEO_FILE, format="h264", quality=23)
        except Exception as exc:
            self.camera.close()
            logger.debug(traceback.format_exc())
            logger.info(exc)
            logger.error("Error in starting camera")
            return False

        try:
            self.arduino.say(tweet["Text"])
        except Exception as exc:
            self.camera.close()
            logger.debug(traceback.format_exc())
            logger.info(exc)
            logger.error("Fail in Arduino comm.")
            return False

        logger.debug("Stopping recording")
        self.camera.stop_recording()
        self.camera.close()
        time_stop = time.time()

        # Add some random scaling factor, because videos turn out to be longer than Python timing
        time_video = (time_stop - time_start) * 1.206
        try:
            logger.info("Recording length is %d seconds" % time_video)
        except FileNotFoundError:
            logger.critical("'ffmpeg' not installed! Exiting..")
            sys.exit()

        if time_video < 30:

            # Put raw video into MP4 container
            logger.info("Calling ffmpeg..")
            # Capture output, so it doesn't clog the screen
            p = subprocess.run(ENCODE_CMD, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
            if p.returncode == 0:
                logger.info("Video conversion done")
            else:
                # Set error log level in the ENCODE_CMD
                logger.error("ffmpeg failed with code: %d" % p.returncode)
                logger.debug(p.stderr)
                return False

            # Post the video to Twitter
            message = self.get_reply_message()
            try:
                self.tw.post_reply(message, tweet,
                                    video_file=VIDEO_FILE2)
            except Exception as exc:
                logger.debug(traceback.format_exc())
                logger.info(exc)

                logger.error("Some error while posting Twitter video")
                return False

            logger.info("Succesfully posted video tweet")
            return True

        else:
            logger.error("Recording too long! Discarding..")

            message = ("Unfortunately Twitter only allows 30s video. "
                       "Your message was %ds :(" % time_video)
            try:
                tw.post_reply(message, tweet)
            except Exception as exc:
                logger.debug(traceback.format_exc())
                logger.info(exc)

                logger.error("Some error while posting a regular Tweet")
                return False

            logger.info("Succesfully posted a reply tweet")
            return True

    def get_reply_message(self):
        """Return a text message that is attached to the reply video"""
        # TODO: Make this something interesting
        return "You say and I reply :)"

    def run(self):
        """Main program loop"""
        q = queue.Queue();

        # Launch REST API Search thread
        scrubber = self.tw.start_old_message_scrubber(q, interval=60)

        # Launch Twitter Streaming thread
        streamer = self.tw.start_stream(q)

        while(True):
            logger.debug("There are %d items in the queue" %(q.qsize()))
            if q.empty():
                time.sleep(10)
                continue
            else:
                tweet = q.get()

            retcode = self.show_tweet(tweet)
            if not retcode:
                logger.warning("Putting tweet back into queue due to errors")
                q.put(tweet)
                time.sleep(2)

            if not streamer.isAlive():
                logger.warning("Streamer thread exited. Restarting..")
                streamer = self.tw.start_stream(q)

            if not scrubber.isAlive():
                logger.warning("REST scrubber exited. Restarting..")
                scrubber  =self.tw.start_old_message_scrubber(q, interval=60)

        self.arduino.close()


if __name__ == "__main__":
    # logger.basicConfig(level=logger.DEBUG)
    twitter_handler_logger = logging.getLogger('twitter_handler')
    twitter_handler_logger.setLevel(logging.DEBUG)

    arduino_handler_logger = logging.getLogger('arduino_handler')
    arduino_handler_logger.setLevel(logging.DEBUG)

    main_logger = logging.getLogger('MAIN')
    main_logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s :%(filename)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    twitter_handler_logger.addHandler(handler)
    arduino_handler_logger.addHandler(handler)

    app = TwitterParrot()
    app.run()
