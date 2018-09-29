import os
bind = '0.0.0.0:5001'
workers = 1
backlog = 2048
worker_class = "sync"
debug = True
proc_name = 'brun.gunicorn.proc'
pidfile = 'brun.gunicorn.pid'
#logfile = 'error.brun.log'
errorlog = 'brun.error.log'
loglevel = 'debug'
raw_env = ["FLASK_CONFIG=production"]
accesslog = 'brun.access.log'
access_log_format= '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
daemon = True