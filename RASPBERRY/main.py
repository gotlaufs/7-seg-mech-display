#!/usr/bin/env python3
""" Main Parrot app """

import time
import logging
import subprocess
import picamera
import arduino_handler

VIDEO_FILE = "video.h264"
VIDEO_FILE2 = "video.mp4"
# Use ffmpeg to put raw h.264 video in mp4 container with no re-encodeing
# 'y' to all questions
ENCODE_CMD = ["ffmpeg", "y", "-i", VIDEO_FILE, "-c", "copy", VIDEO_FILE2]


def main():
    arduino = arduino_handler.ArduinoHandler()
    camera = picamera.PiCamera()
    camera.resolution = (1280, 720)

    print("Resolution = ", camera.resolution)
    print("FPS = ", camera.framerate)

    logging.debug("Starting recording")
    start = time.time()
    camera.start_recording(VIDEO_FILE, format="h264", quality=23)
    stop = time.time()
    print("Time to start recording: ", stop - start)
    arduino.say("Hello")
    arduino.close()
    logging.debug("Stopping recording")
    camera.stop_recording()

    logging.info("Calling ffmpeg..")
    p = subprocess.run(ENCODE_CMD)
    if p.returncode == 0:
        logging.info("Video conversion done")
    else:
        logging.error("ffmpeg failed with code: %d" % p.returncode)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
