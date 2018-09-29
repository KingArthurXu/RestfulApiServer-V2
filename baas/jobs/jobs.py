#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'

import time
from datetime import datetime
# from manage import app
import os
import subprocess
import logging
from flask import current_app

logging.basicConfig()
logger_jobs = logging.getLogger('jobs')


def job1(job_id, *params):
    from manage import app
    app.app_context().push()
    # global job_output, job_run_at, job_finish_at
    job_run_at = datetime.now()
    # print(str(a) + ' ' + str(b))
    # print current_app._get_current_object()
    job_output = params[0] + ' ' + params[1]
    # print("job1 end")
    job_finish_at = datetime.now()
    save_job_logs(job_id, job_run_at, job_finish_at, job_output)


def mail_sent_job_logs(recipient, job_id, job_run_at, job_finish_at, job_output):
    from flask_mail import Message
    from manage import mail
    from manage import app
    app.app_context().push()
    recipients = [recipient]
    body = "job_id    : " + job_id +\
           "\nrun_at    : " + str(job_run_at) +\
           "\nfinish_at : " + str(job_finish_at) +\
           "\n-----------------------------------------" +\
           "\nOutput    : " + job_output

    msg = Message(
                  # sender=app.config['FLASKY_MAIL_SENDER'],
                  # sender="3540710@qq.com",
                  recipients=recipients,
                  subject="scheduled jobs" + str(job_run_at), body=body)
    mail.send(msg)


def mail_shell_job(job_id, *params):
    from manage import app
    app.app_context().push()
    # global job_output, job_run_at, job_finish_at
    job_run_at = datetime.now()
    job_output = ''
    try:
        shell_params = list(params)
        recipient = shell_params.pop(0)
        shell_params[0] = os.path.join(current_app.root_path, current_app.config['UPLOAD_DIR'], shell_params[0])
        # print shell_params
        with open(os.devnull, 'w') as FNULL:
            child = subprocess.Popen(shell_params, stdout=subprocess.PIPE, stderr=FNULL)
            job_output = child.communicate()[0]
            # print job_output
    except Exception as e:
        logger_jobs.error(e)
    finally:
        job_finish_at = datetime.now()
        save_job_logs(job_id, job_run_at, job_finish_at, job_output)
        # sending email log
        mail_sent_job_logs(recipient, job_id, job_run_at, job_finish_at, job_output)


def shell_job(job_id, *params):
    from manage import app
    app.app_context().push()
    # global job_output, job_run_at, job_finish_at
    job_run_at = datetime.now()
    job_output = ''
    try:
        shell_params = list(params)
        shell_params[0] = os.path.join(current_app.root_path, current_app.config['UPLOAD_DIR'], params[0])
        # print shell_params
        with open(os.devnull, 'w') as FNULL:
            child = subprocess.Popen(shell_params, stdout=subprocess.PIPE, stderr=FNULL)
            job_output = child.communicate()[0]
            # print job_output
    except Exception, e:
        logger_jobs.error(shell_params)
        logger_jobs.error(e)
    finally:
        job_finish_at = datetime.now()
        save_job_logs(job_id, job_run_at, job_finish_at, job_output)


def db_shell_job(job_id, *params):
    from manage import app
    app.app_context().push()
    # global job_output, job_run_at, job_finish_at
    job_run_at = datetime.now()
    job_output = ''
    try:
        shell_params = list(params)
        shell_params[0] = os.path.join(current_app.root_path, current_app.config['UPLOAD_DIR'], params[0])
        # print shell_params
        with open(os.devnull, 'w') as FNULL:
            child = subprocess.Popen(shell_params, stdout=subprocess.PIPE, stderr=FNULL)
            job_output = child.communicate()[0]
            # print job_output
    except Exception as e:
        logger_jobs.error(e)
    finally:
        job_finish_at = datetime.now()
        save_job_logs(job_id, job_run_at, job_finish_at, job_output)
        db_save_job_logs(job_id, job_run_at, job_finish_at, job_output)


def save_job_logs(job_id, job_run_at, job_finish_at, job_output):
    from manage import app
    app.app_context().push()
    logger_jobs.debug("\njob_id    : " + job_id +
                    "\nrun_at    : " + str(job_run_at) +
                    "\nfinish_at : " + str(job_finish_at) +
                    "\nOutput    : " + job_output +
                    "\n-----------------------------------------")


def db_save_job_logs(job_id, job_run_at, job_finish_at, job_output):
    from manage import app, db
    app.app_context().push()
    from baas.models.dbs import ApsJobLogs
    log = ApsJobLogs(job_id=job_id, run_at=job_run_at, finish_at=job_finish_at, output=job_output)


    db.session.add(log)
    db.session.commit()


