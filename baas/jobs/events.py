#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'
# from App.models.dbs import *
# from run import scheduler
# from App.models import dbs
from apscheduler.events import *
# from App.jobs import jobs
# from datetime import datetime

def save_events(events):
    pass
    # with scheduler.app.app_context():
    #     #print("app_context")
    #     job = APScheduleJob.query.filter_by(jobid=events.job_id).first()
    #     if job is None:
    #         #print("job is not , init it")
    #         job = APScheduleJob(jobid=events.job_id, jobruntimes = 0, jobname=events.job_id)
    #         job.add_run_time()
    #         db.session.add(job)
    #         #test user
    #         user = User(username='john',password='cat')
    #         db.session.add(user)
    #         db.session.commit()
    #
    #     else:
    #         #print("job exist, update")
    #         job.add_run_time()
    #         db.session.add(job)
    #         db.session.commit()

# LISTENER_JOB = (EVENT_JOB_ADDED |
#                 EVENT_JOB_REMOVED |
#                 EVENT_JOB_MODIFIED |
#                 EVENT_JOB_EXECUTED |
#                 EVENT_JOB_ERROR |
#                 EVENT_JOB_MISSED)


# def save_job_logs(events):
#     from App.jobs import jobs
#     from App.models.db import ApsJobLogs
#     log = ApsJobLogs(job_id=events.job_id, run_at=jobs.job_run_at, finish_at=jobs.job_finish_at, output=jobs.job_output)
#     from run import db
#     db.session.add(log)
#     db.session.commit()


def events_listener(events):
    if events.code == EVENT_JOB_MISSED:
        pass
        # print("Job missed id in: %s " % str(events.job_id))
        # save_events(events)
    elif events.code == EVENT_JOB_EXECUTED:
        pass
        # print("Job executed id in: %s " % str(events.job_id))
        # job_id = events.job_id
        # save_job_logs(events)

