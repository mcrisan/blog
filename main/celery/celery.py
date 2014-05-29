from __future__ import absolute_import

from celery import Celery

cel_app = Celery()
cel_app.config_from_object('celeryconfig')

if __name__ == '__main__':
    cel_app.start()