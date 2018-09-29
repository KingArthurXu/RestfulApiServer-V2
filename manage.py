#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'
import os
from config import config
from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from flask_mail import Mail
from apscheduler.events import *
from baas.jobs.events import events_listener
from exceptions import Exception
import logging.config
from flask_script import Manager, Shell
# from flask_migrate import Migrate, MigrateCommand

from baas.models.dbs import db, ApsJobs, User, Role, ShellFile
#
#  500 : { "message": "An unhandled exception occurred." } http://192.168.92.139:5000/swagger.json
#
import sys
reload(sys)
sys.setdefaultencoding('utf8')


logging.config.fileConfig('logging.conf')
logging.info('logging starts')

app = Flask(__name__)
# 读Flask配置文件
os.getenv("config_name")
config_name = os.getenv("FLASK_CONFIG") if os.getenv("FLASK_CONFIG") else 'production'
app.config.from_object(config[config_name])

db.init_app(app)

# 让python支持命令行工作
manager = Manager(app)

# 使用migrate绑定app和db
# migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中init
# manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, ShellFile=ShellFile, ApsJobs=ApsJobs)

manager.add_command("shell", Shell(make_context=make_shell_context))

# import flask_monitoringdashboard as dashboard
# dashboard.bind(app)

# from flask_cors import CORS
# CORS(app)有

# 配置邮件
mail = Mail(app)

# 创建数据库, 迁移到models\db
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# 定时任务
LISTENER_JOB = (EVENT_JOB_ADDED |
                EVENT_JOB_REMOVED |
                EVENT_JOB_MODIFIED |
                EVENT_JOB_EXECUTED |
                EVENT_JOB_ERROR |
                EVENT_JOB_MISSED)

scheduler = APScheduler()
scheduler.init_app(app)


# from baas.models.dbs import *
# from baas.models.views import *

# 后台管理
# move to brun.py
# admin = Admin(app, name=u'baas AP Server 后台管理系统', template_mode='bootstrap3')
# admin.add_view(UserView(User, db.session, name=u'用户管理'))
# admin.add_view(RoleView(Role, db.session, name=u'权限管理'))
# admin.add_view(ShellFileView(ShellFile, db.session,name=u'Shell文件管理'))
# admin.add_view(ShellParamView(ShellParam, db.session, name=u'Shell参数配置'))
# admin.add_view(ApsJobView(ApsJobs, db.session, name=u'后台Job配置'))
# admin.add_view(ApsJobLogsView(ApsJobLogs, db.session, name=u'后台Job运行日志'))
# admin.add_view(MyLoginView(name='Login_myadmin'))
# admin.add_view(MyLogoutView(name='Logout'))

# from baas.models import init_database, init_jobs
# if app.config['INIT_DB']:
#     init_database(app, db)
#     db.session.commit()
# else:
#     init_jobs(app, db)
# Flask-Security
from baas.models.dbs import db, User, Role, ShellFile, ApsJobs
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security().init_app(app, user_datastore, register_blueprint=False)

# move to frun
# from baas.others.upload import site_blueprint
# from baas.endpoints import api_blueprint
# app.register_blueprint(blueprint=api_blueprint)
# app.register_blueprint(blueprint=site_blueprint)


# @app.errorhandler
#      def not_found(error):
#          return render_template('errors/404.html'), 404

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return db.session.query(User).filter(User.id == userid).first()
    except Exception as e:
        return None


def init_database():
    # 创建Shell目录
    file_path = os.path.join(app.root_path, app.config['UPLOAD_DIR'])
    try:
        os.mkdir(file_path)
    except OSError:
        pass

    db.drop_all()
    # 创建表
    db.create_all()
    user_test1 = User(username=u"test1", password=u"test1")
    user_test2 = User(username=u"test2", password=u"test2")
    user_string = User(username=u"string", password=u"string")
    user_admin = User(username=u"admin", password=u"ad")
    role_admin = Role(name=u"admin", description=u"admin")

    shell1 = ShellFile(name=u"bp.sh", path=u"bp.sh")
    shell2 = ShellFile(name=u"before.sh", path=u"before.sh")
    shell3 = ShellFile(name=u"after.sh", path=u"after.sh")

    aps_jobid='[baas.jobs.jobs:job1-1]'
    job1 = ApsJobs(aps_jobid=aps_jobid, aps_func='baas.jobs.jobs:job1', aps_args='888 888',
                   aps_tirgger='cron', aps_cron='*/2 * * * * * *')
    aps_jobid = '[baas.jobs.jobs:shell_job]'
    job2 = ApsJobs(aps_jobid='[baas.jobs.jobs:shell_job]', aps_func='baas.jobs.jobs:shell_job', aps_args='bp.bat 999 999',
                   aps_tirgger='cron', aps_cron='*/2 * * * * * *')

    from flask_sqlalchemy import event
    # @event.listens_for(db.session, "after_flush", once=True)
    # def receive_after_flush(session, context):
    session = db.create_session({})()
    session.add(user_test1)
    session.add(user_test2)
    session.add(user_string)
    session.add(user_admin)

    # https://stackoverflow.com/questions/45044926/db-model-vs-db-table-in-flask-sqlalchemy
    user_admin.roles.append(role_admin)
    session.add(role_admin)
    session.add(job1)
    session.add(job2)
    session.add(shell1)
    session.add(shell2)
    session.add(shell3)
    session.commit()


def init_jobs():
    from baas.models.dbs import ApsJobs
    # session
    # with app.app_context():
    app.app_context().push()
    apsjob_all = ApsJobs.query.all()
    for item in apsjob_all:
        logging.warning("Add Job <" + item.aps_jobid + "> " + item.aps_func)
        from collections import namedtuple
        CRON = namedtuple('CRON', ['second', 'minute', 'hour', 'day', 'month', 'day_of_week', 'year'])
        import shlex
        if item.aps_cron:
            cron_args = CRON(*shlex.split(item.aps_cron))._asdict()
        scheduler.add_job(id=item.aps_jobid, func=item.aps_func,
                          args=shlex.split(item.aps_jobid + ' ' + item.aps_args),
                          trigger=item.aps_tirgger, minute=cron_args['minute'], hour=cron_args['hour'],
                          day=cron_args['day'], month=cron_args['month'], day_of_week=cron_args['day_of_week'],
                          year=cron_args['year'], second=cron_args['second'])
        if not item.job_enabled:
            logging.warning("Pause Job <" + item.aps_jobid + "> " + item.aps_func)
            scheduler.pause_job(id=item.aps_jobid)
    # pass

if __name__ == '__main__':
    manager.run()
