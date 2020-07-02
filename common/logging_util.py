"""
Use this to enable logging outside of Django

Example usage:
from common.django_needed import logging_util

    # Setup daemon logging
    daemon_name = "ExampleDaemon"
    self.logger = logging_util.get_logger(daemon_name)
    self.logger.debug('This is a debug message in the daemon log.')

    # Switch to log with a different name and do a roll over
    logging_util.set_logger_config("job_log_name")
    logger.debug('This is a debug message in the job log.')
    logging_util.force_log_rollover(logger) # start with a clean log
    logger.error('This is an error message in a new job log.')

    # Switch back to daemon logging
    logging_util.set_logger_config(daemon_name)
    logger.debug('This is a debug message in the daemon log.')
"""
from copy import deepcopy
import logging
from logging import config
import os
import socket

from common import constants

LOGGING_CONF = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(module)s::%(funcName)s::%(lineno)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
            'level': 'DEBUG',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'verbose',
        },
        'logfile': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
            'filename': '<PATH/FILENAME SET USING function::get_logger()>',
            'mode': 'a',
            'maxBytes': 1024 * 1024 * 100,  # 100 MB
            'backupCount': 4,
            'encoding': 'utf8',
        },
        'error_email': {
            'class': 'logging.handlers.SMTPHandler',
            'level': 'CRITICAL',
            'formatter': 'verbose',
            'mailhost': constants.SMTP_SERVER,
            'fromaddr': "someone@something.com",
            'toaddrs': ["someone1@something.com", "someone2@something.com", ],
            'subject': '<SUBJECT SET USING function::get_logger()>',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'logfile', 'error_email'],
            'level': 'DEBUG' if constants.DEBUG else 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console', 'logfile', 'error_email'],
            'level': 'DEBUG' if constants.DEBUG else 'ERROR',
            'propagate': False,
        },
    }
}


def set_logger_config(log_name):
    """
    Pass in your log_name and set the logger config.
    NOTE: Use to switch log names.

    :param log_name: log name to be used for the log
    """
    logging_conf = deepcopy(LOGGING_CONF)

    subject = "{0} CRITICAL Error on {1}".format(log_name, socket.gethostname())
    logging_conf["handlers"]["error_email"]["subject"] = subject

    log_path_name = os.path.join(constants.LOG_DIR, ("{0}.log".format(log_name)))
    logging_conf["handlers"]["logfile"]["filename"] = log_path_name

    logging.config.dictConfig(logging_conf)


def get_logger(log_name):
    """
    Pass in your log_name and get back a logger.
    NOTE: Use to get a logger with the log_name.

    :param log_name: log name to be used for the log
    :return: logger
    """
    set_logger_config(log_name)
    logger = logging.getLogger(__name__)
    return logger


def force_log_rollover(logger):
    """
    This will access the handler that is configured as a RotatingFileHandler and force a rollover.

    :param logger: logger that you are using to write logs
    :return boolean: True if successful else false
    """
    rolled_over = False

    for handle in logger.root.handlers:
        if handle.name == "logfile":
            handle.doRollover()
            rolled_over = True
            break

    return rolled_over
