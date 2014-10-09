# coding=utf-8
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_socketio_test.settings")
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        from socketio.server import SocketIOServer
        server = SocketIOServer(('', 8001), application, resource="socket.io")
        server.serve_forever()