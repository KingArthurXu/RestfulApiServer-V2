#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'

import logging

from App.security import auth_token_required, roles_required
from flask_restplus import Resource, reqparse, fields, Namespace
from flask_security import login_user
from App.restapi.endpoints.popen import exec_command
from sqlalchemy.orm.exc import NoResultFound

from App.database.models import User

log = logging.getLogger(__name__)
ns_bpdbjobs = Namespace('bpdbjobs', description='bpdbjobs – 与 NetBackup 作业数据库进行交互')


@ns_bpdbjobs.route('/bpdbjobs')
class Login(Resource):  # 自定义登录函数

    # 需要安全登陆信息
    # @auth_token_required
    def post(self):
        out = exec_command()
        return {"message": "用户名或密码错误"}, 401

    def get(self):
        raise NoResultFound

