""" Mock Arduino serial handler """
import logging
import time


class ArduinoHandler():
    """Class to interface with Arduino FW"""
    BAUD = 9600
    MAX_MESSAGE_LEN = 200
    DEFAULT_PORT = "/dev/ttyUSB0"
    TERM_CHAR = b"\n"
    # How long to wait for Raspberry to process UART requests
    SERIAL_DELAY = 0.5
    SERIAL_TIMEOUT = 2  # How long to wait for serial messages

    # Default Arduino values. Used for calculating timeout for UART read
    LETTER_DELAY = 500
    WORD_DELAY = 1000
    DRIVE_TIME = 250
    BLANK = False

    def __init__(self, port=None):
        """Initializer

        If you pass 'port' argument, it wil be used as the port name, otherwise
        the default is used"""
        pass

    def say(self, message):
        """Make the display say something"""
        time.sleep(len(message) * 0.05)

    def blank(self, state=False):
        """Turn the blanking between characters ON or OFF"""
        if state is True:
            data = "BLANK ON"
        elif state is False:
            data = "BLANK OFF"
        else:
            raise ArduinoHandlerError("Invalid blank state: <%s>" % state)


    def letter_delay(self, delay):
        """Set the delay between displaying characters

        'delay' is in milliseconds"""
        delay = abs(int(delay))

        data = "LETTER_DELAY " + str(delay)

    def word_delay(self, delay):
        """Set the delay between displaying words

        'delay' is in milliseconds"""
        delay = abs(int(delay))

        data = "WORD_DELAY " + str(delay)


    def close(self):
        """Do cleanup"""
        if self.port.is_open:
            logging.info("Closing serial port..")
            self.port.close()
        else:
            logging.warning("Tried to close serial port that is not open")

    def _send_bytes(self, string):
        """Actual sending of Bytes.

        Arduino is always brought into a known state before sending"""
        pass

    def _reply_check(self, timeout=None):
        """Check the status of the Arduino reply"""
        pass


class ArduinoHandlerError(Exception):
    """Simple error class for passing errors"""
    pass
