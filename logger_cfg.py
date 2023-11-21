import logging

def configure_logger():
    logger = logging.getLogger('Logger')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('logs/flask.log')
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger