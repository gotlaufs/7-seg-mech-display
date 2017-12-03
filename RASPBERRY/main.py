#!/usr/bin/env python3
""" Main Parrot app """

import time
import logging
import picamera
import arduino_handler

VIDEO_FILE = "video.h264"


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

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
