# coding=utf-8
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from django.core.wsgi import get_wsgi_application
        from socketio.server import serve

        application = get_wsgi_application()
        serve(application, port=8001)
