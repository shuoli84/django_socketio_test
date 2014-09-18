import gevent
from socketio.decorators import namespace
import logging

logger = logging.getLogger(__name__)


print 'hello'

@namespace('/echo')
class EchoNamespace(object):

    @classmethod
    def on_message(cls, socket, message):
        logger.info('received new message %s', message)
        socket.emit('message', message)

        def loop():
            while True:
                socket.emit('message', 'hello')
                gevent.sleep(2)

        cls.job = gevent.spawn(loop)

    @classmethod
    def on_stop_message(cls, socket, message):
        gevent.kill(cls.job)