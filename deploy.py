# -*- coding: latin-1 -*-
from gevent.pywsgi import WSGIServer
from main import app

http_server = WSGIServer(('', 80), app)
http_server.serve_forever()
