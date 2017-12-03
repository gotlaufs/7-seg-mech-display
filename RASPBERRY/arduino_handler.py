""" Arduino serial handler """
import serial
import logging
import time


class ArduinoHandler():
    """Class to interface with Arduino FW"""
    self.BAUD = 9600
    self.MAX_MESSAGE_LEN = 200
    self.DEFAULT_PORT = "/dev/ttyUSB0"
    self.TERM_CHAR = b"\n"
    # How long to wait for Raspberry to process UART requests
    self.SERIAL_DELAY = 0.1
    self.SERIAL_TIMEOUT = 2  # How long to wait for serial messages

    # Default Arduino values. Used for calculating timeout for UART read
    self.LETTER_DELAY = 500
    self.WORD_DELAY = 1000
    self.DRIVE_TIME = 250
    self.BLANK = False

    def __init__(self, port=None):
        """Initializer

        If you pass 'port' argument, it wil be used as the port name, otherwise
        the default is used"""
        self.port = serial.Serial()
        self.port.baudrate = self.BAUD
        self.port.timeout = self.SERIAL_TIMEOUT

        if port is None:
            logging.info("No port specified, setting to <%s>"
                         % self.DEFAULT_PORT)
            self.port.port = self.DEFAULT_PORT
        else:
            self.port.port = port

        # Open the serial port for writing
        loging.debug("Trying to open serial port <%s>.." % self.port.port)
        self.port.open()

    def say(self, message):
        """Make the display say something"""
        if len(message) > self.MAX_MESSAGE_LEN:
            logging.error("Message too long (%d), trimming to (%d)"
                          % (len(message), self.MAX_MESSAGE_LEN))
            message = message[0:self.MAX_MESSAGE_LEN]

        # Calculate the approximate time it will take to disply the message
        spaces = message.count(" ")
        regular_chars = len(message) - spaces

        regular_time = self.DRIVE_TIME * 2 + self.LETTER_DELAY
        space_time = self.DRIVE_TIME * 2 + self.WORD_DELAY

        timeout = regular_chars * regular_time
        timeout += spaces * space_time
        if self.BLANK is True:
            timeout += len(message) * regular_time

        timeout = timeout/1000
        logging.debug("Calculated display time for message is %.2f s"
                      % timeout)

        old_timeout = self.port.timeout
        self.port.timeout = timeout + 1  # Add some margin

        data = "SAY " + message
        self._send_bytes(data)
        self.port.timeout = old_timeout
        logging.debug("Restored old UART read timeout: %.2f" % old_timeout)

    def blank(self, state=False):
        """Turn the blanking between characters ON or OFF"""
        if state is True:
            data = b"BLANK ON"
        elif state is False:
            data = b"BLANK OFF"
        else:
            raise ArduinoHandlerError("Invalid blank state: <%s>" % state)

        self._send_bytes(data)
        self.BLANK = state

    def letter_delay(self, delay):
        """Set the delay between displaying characters

        'delay' is in milliseconds"""
        delay = abs(int(delay))

        data = "LETTER_DELAY " + str(delay)
        self._send_bytes(data)
        self.LETTER_DELAY = delay

    def word_delay(self, delay):
        """Set the delay between displaying words

        'delay' is in milliseconds"""
        delay = abs(int(delay))

        data = "WORD_DELAY " + str(delay)
        self._send_bytes(data)
        self.WORD_DELAY = delay

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
        self.port.write(self.TERM_CHAR)
        time.sleep(self.SERIAL_DELAY)
        self.port.reset_input_buffer()
        logging.debug("Sending message: <%s>" % string)
        self.port.write(string.encode())

    def _reply_check(self):
        """Check the status of the Arduino reply"""
        time.sleep(self.SERIAL_DELAY)
        line = self.port.readline()
        line = decode(line)

        if "OK" in line:
            logging.debug("Got an OK response")
            return line
        elif "ERROR" in line:
            rem_bytes = self.port.in_waiting()
            data = self.read(rem_bytes)
            data = decode(data)
            line += data
            raise ArduinoHandlerError(line)
        else:
            raise ArduinoHandlerError("Unknown error, message = <%s>" % line)


class ArduinoHandlerError(Exception):
    """Simple error class for passing errors"""
    pass
