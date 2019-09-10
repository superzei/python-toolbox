import logging


def new_logger(name: str, console_log=True, file_log=True, filename="logger/LOG.log") -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.handlers = []

    if console_log:
        c_handler = logging.StreamHandler()
        c_format = logging.Formatter('[%(levelname)s] [%(name)s] - %(message)s')
        c_handler.setLevel(logging.INFO)
        c_handler.setFormatter(c_format)
        logger.addHandler(c_handler)

    if file_log:
        assert filename is not None  # safety
        f_handler = logging.FileHandler(filename)
        f_format = logging.Formatter('%(asctime)s - [%(levelname)s] [%(name)s] - %(message)s')
        f_handler.setLevel(logging.INFO)
        f_handler.setFormatter(f_format)
        logger.addHandler(f_handler)

    return logger