import logging


class CustomFormatter(logging.Formatter):

    grey     = "\x1b[38;20m"
    green    = "\x1b[32;20m"
    yellow   = "\x1b[33;20m"
    red      = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset    = "\x1b[0m"
    format   = "%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

    FORMATS = {logging.DEBUG: grey + format + reset,
               logging.INFO: green + format + reset,
               logging.WARNING: yellow + format + reset,
               logging.ERROR: red + format + reset,
               logging.CRITICAL: bold_red + format + reset}

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno)
        formatter  = logging.Formatter(log_format)
        return formatter.format(record)


def get_logger(name: str | None = 'App_Name',
               stduot=True):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if stduot:
        main_handler = logging.StreamHandler()
    else:
        main_handler = logging.FileHandler('log')
    main_handler.setLevel(logging.DEBUG)
    main_handler.setFormatter(CustomFormatter())
    logger.addHandler(main_handler)
    return logger