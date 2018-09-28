""" Arduino serial handler """
import serial
import logging
import time

logger = logging.getLogger(__name__)

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
        self.port = serial.Serial()
        self.port.baudrate = self.BAUD
        self.port.timeout = self.SERIAL_TIMEOUT

        if port is None:
            logger.info("No port specified, setting to <%s>"
                         % self.DEFAULT_PORT)
            self.port.port = self.DEFAULT_PORT
        else:
            self.port.port = port

        # Open the serial port for writing
        logger.debug("Trying to open serial port <%s>.." % self.port.port)
        self.port.open()
        time.sleep(2)
        self.port.reset_input_buffer()

    def say(self, message):
        """Make the display say something"""
        if len(message) > self.MAX_MESSAGE_LEN:
            logger.error("Message too long (%d), trimming to (%d)"
                          % (len(message), self.MAX_MESSAGE_LEN))
            message = message[0:self.MAX_MESSAGE_LEN]

        # Calculate the approximate time it will take to disply the message
        spaces = message.count(" ")
        regular_chars = len(message) - spaces

        regular_time = self.DRIVE_TIME + self.LETTER_DELAY
        space_time = self.DRIVE_TIME + self.WORD_DELAY

        timeout = regular_chars * regular_time
        timeout += spaces * space_time
        if self.BLANK is True:
            timeout += len(message) * regular_time

        timeout = timeout/1000
        logger.debug("Calculated display time for message is %.2f s"
                      % timeout)

        data = "SAY " + message

        self._send_bytes(data)
        self._reply_check(timeout + 1)  # Add some time margin

    def blank(self, state=False):
        """Turn the blanking between characters ON or OFF"""
        if state is True:
            data = "BLANK ON"
        elif state is False:
            data = "BLANK OFF"
        else:
            raise ArduinoHandlerError("Invalid blank state: <%s>" % state)

        self._send_bytes(data)
        self._reply_check()
        self.BLANK = state
        logger.debug("Set BLANK to %s" % state)

    def letter_delay(self, delay):
        """Set the delay between displaying characters

        'delay' is in milliseconds"""
        delay = abs(int(delay))

        data = "LETTER_DELAY " + str(delay)
        self._send_bytes(data)
        self._reply_check()
        self.LETTER_DELAY = delay
        logger.debug("Set LETTER_DELAY to %d ms" % delay)

    def word_delay(self, delay):
        """Set the delay between displaying words

        'delay' is in milliseconds"""
        delay = abs(int(delay))

        data = "WORD_DELAY " + str(delay)
        self._send_bytes(data)
        self._reply_check()
        self.WORD_DELAY = delay
        logger.debug("Set WORD_DELAY to %d ms" % delay)

    def close(self):
        """Do cleanup"""
        if self.port.is_open:
            logger.info("Closing serial port..")
            self.port.close()
        else:
            logger.warning("Tried to close serial port that is not open")

    def _send_bytes(self, string):
        """Actual sending of Bytes.

        Arduino is always brought into a known state before sending"""
        self.port.write(self.TERM_CHAR)
        time.sleep(self.SERIAL_DELAY)
        self.port.reset_input_buffer()
        logger.debug("Sending message: <%s>" % string)
        string += "\n"
        self.port.write(string.encode())

    def _reply_check(self, timeout=None):
        """Check the status of the Arduino reply"""
        if timeout is None:
            timeout = self.SERIAL_DELAY
        time.sleep(timeout)
        line = self.port.readline()
        line = line.decode()

        if "OK" in line:
            logger.debug("Got an OK response")
            return line
        else:
            rem_bytes = self.port.in_waiting
            data = self.port.read(rem_bytes)
            data = data.decode()
            line += data
            raise ArduinoHandlerError(line)


class ArduinoHandlerError(Exception):
    """Simple error class for passing errors"""
    pass
