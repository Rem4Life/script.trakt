# custom_logger.py
import logging
import logging.handlers


def setup_logging_client():
    root_logger = logging.getLogger()
    socket_handler = logging.handlers.SocketHandler("localhost", 9000)
    root_logger.addHandler(socket_handler)
    root_logger.setLevel(logging.DEBUG)


def get_logger(name):
    logger = logging.getLogger(name)
    return logger


if __name__ == "__main__":
    setup_logging_client()
    logger = get_logger("TestLogger")

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
