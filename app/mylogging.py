"This module contains the logging configuration for the webserver."
import logging
from logging.handlers import RotatingFileHandler
import time


def configure_logger():
    """This function configures the logger."""
    # Creez un logger si il configurez pentru nivelul INFO
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # Creez un handler care scrie in fisierul webserver.log
    handler = RotatingFileHandler(
        'webserver.log',
        mode='w',
        maxBytes=10000,
        backupCount=5)
    # Formatez mesajele de log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # Timpul este cel GMT
    formatter.formatTime = lambda record, datefmt: time.strftime(
        '%Y-%m-%d %H:%M:%S GMT', time.localtime(record.created))
    handler.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(handler)
    return logger
