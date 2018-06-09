#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'

from App.task import celery, mail


@celery.task
def my_background_task(arg1, arg2):
    # some long running task here
    return 12


@celery.task
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

