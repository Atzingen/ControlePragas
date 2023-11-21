# -*- coding: latin-1 -*-
from gevent.pywsgi import WSGIServer
from main import app
from logger_cfg import configure_logger

logger = configure_logger()

if __name__ == '__main__':
    http_server = WSGIServer(('', 8080), app)
    logger.info('Iniciando o seriçao com gevent porta 8080')
    http_server.serve_forever()
