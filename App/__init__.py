#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'

from flask import Flask
from flask_security import SQLAlchemyUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


app = Flask(__name__)
# 读Flask配置文件
app.config.from_object('settings')

# import flask_monitoringdashboard as dashboard
# dashboard.bind(app)

# from flask_cors import CORS
# CORS(app)有

# 创建Shell目录
file_path = os.path.join(app.root_path, app.config['UPLOAD_DIR'])
# print file_path
# print app.config['UPLOAD_DIR']
try:
    os.mkdir(file_path)
except OSError:
    pass

# 创建数据库
db = SQLAlchemy(app)

from App.endpoints import api_blueprint
app.register_blueprint(blueprint=api_blueprint)

from App.models.db import User, Role, user_to_role, ShellFile
# Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security().init_app(app, user_datastore, register_blueprint=False)

from App.others.upload import site_blueprint
app.register_blueprint(blueprint=site_blueprint)


# 后台管理
from flask_admin import Admin
admin = Admin(app, name=u'BaaS AP Server 后台管理系统', template_mode='bootstrap3')

from App.models.views import UserView, RoleView, ShellFileView, MyLoginView, MyLogoutView
admin.add_view(UserView(User, db.session, name=u'用户管理'))
admin.add_view(RoleView(Role, db.session, name=u'权限管理'))
admin.add_view(ShellFileView(ShellFile, db.session,name=u'Shell文件管理'))

from App.models.db import Person, Address, ShellParam
from App.models.views import ShellParamView
admin.add_view(ShellParamView(ShellParam, db.session, name=u'Shell参数配置'))
admin.add_view(MyLoginView(name='Login_myadmin'))
admin.add_view(MyLogoutView(name='Logout'))


app.secret_key = 'xxxxyyyyyzzzzz'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# @app.errorhandler
#      def not_found(error):
#          return render_template('errors/404.html'), 404



@login_manager.user_loader
def load_user(userid):
    try:
        return db.session.query(User).filter(User.id == userid).first()
    except:
        return None

# init database data
# 删除表
if os.getenv("FLASK_INITDB") == "True":
    db.drop_all()
    #创建表
    db.create_all()

    db.session.add(User(username=u"test1", password=u"test1"))
    db.session.add(User(username=u"test2", password=u"test2"))
    db.session.add(User(username=u"string", password=u"string"))
    user_admin = User(username=u"admin", password=u"ad")
    db.session.add(user_admin)
    role_admin = Role(name=u"admin", description=u"admin")
    db.session.add(role_admin)
    # https://stackoverflow.com/questions/45044926/db-model-vs-db-table-in-flask-sqlalchemy
    user_admin.roles.append(role_admin)

    from App.models.db import ShellFile
    shell1 = ShellFile(name="before.sh", path="before.sh")
    db.session.add(shell1)
    shell2 = ShellFile(name="after.sh", path="after.sh")
    db.session.add(shell2)
    shell3 = ShellFile(name="bp.bat", path="bp.bat")
    db.session.add(shell3)
    db.session.commit()
    # # 自动分析脚本参数
    # from App.endpoints.nbuapi import auto_config_shell_params
    # auto_config_shell_params(shell1.name)
    # auto_config_shell_params(shell2.name)
    # auto_config_shell_params(shell3.name)
    # db.session.commit()