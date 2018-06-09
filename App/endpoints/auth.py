#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'

import logging

from flask_login import current_user
from flask_restplus import Resource, reqparse, fields, Namespace
from flask_security import login_user

from App.endpoints.decorators import auth_token_required, roles_required
from App.models.db import User

log = logging.getLogger(__name__)

ns_auth = Namespace('auth', description='认证接口，获得Token，包括部分基本功能测试API')

#
# 登录并获得Token
login_fields = ns_auth.model('login', {
        'username': fields.String,
        'password': fields.String,
    })


#
# 登录并获得Token
@ns_auth.route('/auth')
class Auth(Resource):  # 自定义登录函数
    @ns_auth.expect(login_fields)
    # 不需要安全登陆信息
    @ns_auth.doc(security=[])
    def post(self):
        u"""
        登陆并获得token
        ```
        {
          "username": "test1",
          "password": "test1"
        }
        ```
        登陆并获得token
        """
        args = reqparse.RequestParser() \
            .add_argument('username', type=str, location='json', required=True, help="用户名不能为空") \
            .add_argument("password", type=str, location='json', required=True, help="密码不能为空") \
            .parse_args()
        user = User.authenticate(args['username'], args['password'])
        if user:
            login_user(user=user)
            return {"message": "登录成功", "token": user.get_auth_token()}, 200
        else:
            return {"message": "用户名或密码错误"}, 401


#
# 刷新Token
@ns_auth.route('/reauth')
class reauth(Resource):  # 自定义登录函数
    @auth_token_required
    @ns_auth.doc(security='apikey')
    def post(self):
        u"""
        利用 Token 来获得新的 Token
        """
        if current_user:
            return {"message": "登录成功", "token": current_user.get_auth_token()}, 200
        else:
            return {"message": "无法刷新"}, 401


#
# 需要Token的API
@ns_auth.route('/protected_sample')
class Protected(Resource):

    @auth_token_required
    @ns_auth.doc(security='apikey')
    @ns_auth.doc(params={'id': 'An ID'})
    def get(self):
        u"""
        需要使用Token，验证用户名后可用
        ```
        id 为可选项，并不会校验
        ```        
        """
        return {"message": "成功！这是需要Token的GET方法"}, 200

    @auth_token_required
    # 需要重新设计
    @roles_required('admin')  # 不满足则跳转至SECURITY_UNAUTHORIZED_VIEW
    # @ns_auth.doc(params={'id': 'An ID'})
    def post(self):
        u"""
        需要使用Token，验证用户必须为Admin才可用
        需要使用Token，验证用户必须为Admin才可用
        """
        return {"message": "成功! 这是需要Token和admin权限的POST方法"}, 201


#
# 测试用方法1
@ns_auth.route('/HelloWorld')
class HelloWorld(Resource):
    @ns_auth.doc(security=[])
    @ns_auth.doc(security='apikey')
    @ns_auth.response(403, 'Not Authorized')
    def get(self):
        u"""
        HelloWorld
        ```
        {
          "username": "test1",
          "password": "test1"
        }
        ```
        HelloWorld 测试API
        """
        # api.abort(403)
        return {'message': 'hello world!'}
