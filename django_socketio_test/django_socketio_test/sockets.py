from socketio.decorators import namespace
import logging

logger = logging.getLogger(__name__)


@namespace('/echo')
class EchoNamespace(object):
    clients = {}

    @classmethod
    def on_connect(cls, socket):
        print 'on connect'
        if socket.id not in cls.clients:
            cls.clients[socket.id] = socket

    @classmethod
    def on_disconnect(cls, socket):
        cls.clients.pop(socket.id, None)

    @classmethod
    def on_message(cls, socket, message):
        print 'received new message %s' % message
        logger.info('received new message %s', message)
        for socket_id, s in cls.clients.items():
            s.emit('message', message)
