import logging


def get_logger(module_name: str) -> logging.Logger:
    return logging.getLogger("solar.%s" % module_name)
