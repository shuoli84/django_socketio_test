# coding=utf-8
from django.core.management.base import BaseCommand
from gevent import monkey
monkey.patch_all()

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "linbang.settings")

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass


class Command(BaseCommand):
    def handle(self, *args, **options):
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
        from socketio.server import SocketIOServer
        server = SocketIOServer(('', 8000), application, resource="socket.io")
        server.serve_forever()