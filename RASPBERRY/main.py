#!/usr/bin/env python3
""" Main Parrot app """

import logging
import arduino_hander


def main():
    arduino = arduino_handler.ArduinoHandler()

    arduino.say("Hello")

    arduino.close()

if __name__ == "__main__":
    main()
