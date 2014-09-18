import json
from unittest import TestCase
import gevent
from gevent.monkey import patch_all
import requests
from socketio.server import serve, SocketIOServer
from socketio.engine.parser import Parser as EngineParser
import socketio.parser as SocketIoParser
from django.core.wsgi import get_wsgi_application
import os

patch_all()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_socketio_test.settings")

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass


def start_server():
    application = get_wsgi_application()
    from socketio.server import SocketIOServer

    server = SocketIOServer(('', 8000), application, resource="socket.io")
    server.serve_forever()


class ServerTest(TestCase):
    def __init__(self, *args, **kwarg):
        patch_all()

        self.host = '127.0.0.1'
        self.port = 8000
        self.root_url = 'http://%(host)s:%(port)d/socket.io/' % {
            'host': self.host,
            'port': self.port
        }
        super(ServerTest, self).__init__(*args, **kwarg)

    def setUp(self):
        self.job = gevent.spawn(start_server)

    def tearDown(self):
        gevent.kill(self.job)

    def test_server(self):
        gevent.sleep(0.5)
        result = {'socket': None}

        def message(socket):
            result['socket'] = socket

            def onevent(packet_data):
                result['packet'] = packet_data

            socket.on('message', onevent)

        SocketIOServer.global_server.namespaces['/'].on('connection', message)

        response = requests.get(self.root_url + '?transport=polling')

        sid = None
        for p, i, t in EngineParser.decode_payload(bytearray(response.content)):
            data = json.loads(p['data'])
            sid = data['sid']
            break

        self.assertIsNotNone(sid)
        self.assertIsNotNone(result['socket'])

        socket_encoded = SocketIoParser.Encoder.encode({
            'type': SocketIoParser.EVENT,
            'data': 'hello'
        })

        engine_encoded = EngineParser.encode_payload({
            'type': 'message',
            'data': socket_encoded[0]
        })

        # Work around the bug which not sending pre buffered message
        response = requests.post(self.root_url + ('?transport=polling&sid=%s' % sid),
                                 data=engine_encoded,
                                 headers={'Content-Type': 'application/octet-stream'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'ok')

        self.assertEqual(result['packet'], 'hello')
