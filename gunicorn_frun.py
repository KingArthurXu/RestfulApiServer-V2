import os
bind = '0.0.0.0:5000'
workers = 4
backlog = 2048
worker_class = "sync"
debug = True
proc_name = 'frun.gunicorn.proc'
pidfile = 'frun.gunicorn.pid'
errorlog = 'frun.error.log'
loglevel = 'debug'
daemon = True
raw_env = ["FLASK_CONFIG=production"]
accesslog = 'frun.access.log'
access_log_format= '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
