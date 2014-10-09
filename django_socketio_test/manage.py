#!/usr/bin/env python
from gevent import monkey
monkey.patch_all()

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_socketio_test.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
