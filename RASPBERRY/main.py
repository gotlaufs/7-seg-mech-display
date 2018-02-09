#!/usr/bin/env python3
""" Main Parrot app """

import time
import logging
import subprocess
import traceback
import sys
import select

import picamera

import arduino_handler
import twitter_handler


# This should work on Raspberry, but just in case adjust as neccessary
ARDUINO_PORT = "/dev/ttyUSB0"

# Pause between main loop iterations
LOOP_DELAY = 15

# If True, will print the whole Python traceback on every handled exception
PRINT_FULL_EXCEPTION = False

# Should not me changed
VIDEO_FILE = "video.h264"
VIDEO_FILE2 = "video.mp4"
# Use ffmpeg to put raw h.264 video in mp4 container with no re-encodeing
# 'y' to all questions
ENCODE_CMD = ["ffmpeg", "-y", "-i", VIDEO_FILE, "-c", "copy", VIDEO_FILE2]

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
        logging.info("Displaying message: %s" % t["Text"])
        logging.info("Starting video recording")
        time_start = time.time()
        self.camera.start_recording(VIDEO_FILE, format="h264", quality=23)
        try:
            self.arduino.say(t["Text"])
        except Exception as exc:
            # TODO: Log error
            if PRINT_FULL_EXCEPTION:
                print(traceback.format_exc())
            print(exc)

            logging.error("Fail in Arduino comm.")
            return

        logging.debug("Stopping recording")
        self.camera.stop_recording()
        time_stop = time.time()

        # Add some random scaling factor, because videos turn out to be longer than Python timing
        time_video = (time_stop - time_start) * 1.206
        logging.info("Recording length is %d seconds" % time_video)
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
                return

            # Post the video to Twitter
            m = self.get_reply_message()
            try:
                self.tw.post_video_reply(message=m, uid=t["ID"],
                                    video_file=VIDEO_FILE2)
            except Exception as exc:
                # TODO: Log exception, not just print
                if PRINT_FULL_EXCEPTION:
                    print(traceback.format_exc())
                print(exc)

                logging.error("Some error while posting Twitter video")
                return

            logging.info("Succesfully posted video tweet")
        else:
            logging.error("Recording too long! Discarding..")

            message = ("Unfortunately Twitter only allows 30s video. "
                       "Your message was %ds :(" % t["video_len"])
            try:
                tw.post_reply(message, t["ID"])
            except Exception as exc:
                # TODO: Log exception, not just print
                if PRINT_FULL_EXCEPTION:
                    print(traceback.format_exc())
                print(exc)

                logging.error("Some error while posting a regular Tweet")
                return

            logging.info("Succesfully posted a reply tweet")

    def get_reply_message(self):
        """Return a text message that is attached to the reply video"""
        # TODO: Make this something interesting
        return "You say and I reply :)"

    def run(self):
        """Main program loop

        1. Get all the old tweets from REST API
        2. Display those
        3. Open Streaming interface and run on that endlessly"""
        # TODO: Restart Streaming interface on errors?
        try:
            statuses = self.tw.get_messages_clean()
        except Exception as exc:
            # TODO: Log exceptions
            if PRINT_FULL_EXCEPTION:
                print(traceback.format_exc())
            print(exc)

            logging.error("Exception while getting tweets! API rate limiting?")
            return

        logging.info("Succesfully got %d tweets from API" % len(statuses))
        self.arduino.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app = TwitterParrot()
    app.run()
