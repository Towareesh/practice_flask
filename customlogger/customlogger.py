class CustomLogger:
    # Template future class for implement different logging level handlers
    # What im want:
    # logger = get_logger(name=__name__)
    # logger.warning('std_OFF', sreaming=False)
    # logger.warning('std_ON', sreaming=True)
    def  __init__(self, name) -> None:
        pass
    
    def file_logger(self):
        pass
    
    def stream_logger(self):
        pass
    
    def get_file_handler(self):
        pass
    
    def get_stream_handler(self):
        pass
    
    def debug(self, message, sreaming):
        pass

    def info(self):
        pass

    def warning(self):
        pass

    def error(self):
        pass

    def critical(self):
        pass