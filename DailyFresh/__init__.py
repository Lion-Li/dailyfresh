from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app
import pymysql


# celery
__all__ = ('celery_app',)


# pymysql
pymysql.install_as_MySQLdb()


