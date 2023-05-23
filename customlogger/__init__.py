import logging
import os
from logging import LogRecord
from logging.handlers import RotatingFileHandler


# def painting(string: str, color: str) -> str:
#     colors = {'red'     : "\x1b[31;20m",
#               'bold_red': "\x1b[31;1m",
#               'green'   : "\x1b[32;20m",
#               'yellow'  : "\x1b[33;20m",
#               'blue'    : "\x1b[34;1m",
#               'gray'    : "\x1b[38;2m"}

#     return f'\x1b[0m{colors[color]}{string}\x1b[0m'


class CustomStreamFormatter(logging.Formatter):
    """Used for custom conversion of the log entry representation to text.

    The custom stream formatter has its own attributes for each logging level.
    Redefined formatting method from the log.The Formatter class is used to
    convert a log entry into color text of a given format.

    Attributes:
        colors: ascii_colors ([color_code;20m)

    DEBUG   : grey color
    INFO    : green color
    WARNING : yellow color
    ERROR   : red color
    CRITICAL: bold red color
    """

    # Color сodes of ascii
    grey     = "\x1b[38;20m"
    green    = "\x1b[32;20m"
    yellow   = "\x1b[33;20m"
    red      = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset    = "\x1b[0m"
    format   = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

    FORMATS = {logging.DEBUG: grey + format + reset,
               logging.INFO: green + format + reset,
               logging.WARNING: yellow + format + reset,
               logging.ERROR: red + format + reset,
               logging.CRITICAL: bold_red + format + reset}

    def format(self, record: logging.LogRecord) -> str:
        """Redefined method to get the required log output format
        """        

        log_format = self.FORMATS.get(record.levelno)
        formatter  = logging.Formatter(log_format)
        return formatter.format(record)


class CustomFileFormatter(CustomStreamFormatter):
    """Used to convert a log entry for writing to a file without using colored lines.
    """

    format = """[%(levelname)s] %(name)s %(asctime)s:\n\tFile "%(filename)s", line %(lineno)d, in %(funcName)s\n%(message)s\n"""

    FORMATS = {logging.DEBUG: format,
               logging.INFO: format,
               logging.WARNING: format,
               logging.ERROR: format,
               logging.CRITICAL: format}
    
    def format(self, record: LogRecord) -> str:
        # Call format method of class CustomStreamFormatter
        return super().format(record)


def get_file_handler():
    # Setup file handler
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # Issue #1: when log file overflow RotatingFileHandler working with error:
    # PermissionError: [WinError 32]
    # temporary solution make log file is infinity.
    # If maxBytes is zero, rollover never occurs
    file_handler = RotatingFileHandler('logs/log.log',
                                       maxBytes=0,
                                       backupCount=0,
                                       encoding='UTF-8')
    file_handler.setFormatter(CustomFileFormatter())
    file_handler.setLevel(logging.DEBUG)
    return file_handler


def get_stream_handler():
    # Setup stream handler (i.e. console)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(CustomStreamFormatter())
    stream_handler.setLevel(logging.DEBUG)
    return stream_handler


def get_logger(sreaming: bool, name: str | None = 'ROOT',) -> logging.Logger:

    logger = logging.getLogger(name)
    # Set general debug level for view all levels
    logger.setLevel(logging.DEBUG)

    if sreaming == True:
        logger.addHandler(get_stream_handler())
    logger.addHandler(get_file_handler())

    return logger