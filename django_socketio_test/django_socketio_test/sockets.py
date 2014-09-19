import gevent
from socketio.decorators import namespace
import logging

logger = logging.getLogger(__name__)


print 'hello'

@namespace('/echo')
class EchoNamespace(object):
    clients = {}

    @classmethod
    def on_join(cls, socket, message):
        if socket.id not in cls.clients:
            cls.clients[socket.id] = socket

    @classmethod
    def on_disconnect(cls, socket, message):
        cls.clients.pop(socket.id, None)

    @classmethod
    def on_message(cls, socket, message):
        logger.info('received new message %s', message)
        for socket_id, s in cls.clients.items():
            s.emit('message', message)
