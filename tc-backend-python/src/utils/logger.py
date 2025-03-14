# logger.py
import logging
import sys

def setup_logger():
    logger = logging.getLogger("chatbot")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(console_handler)

    logger.propagate = False

    return logger

logger = setup_logger()