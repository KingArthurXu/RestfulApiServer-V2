#-*- coding: utf-8 -*-
#!/usr/bin/python
# __author__ = 'Arthur Xu'

import paramiko
from flask_restplus import Resource, reqparse, fields
from App import api, ns

ssh_fields = api.model('ssh_info', {
    'ip': fields.String,
    'port': fields.Integer,
    'username': fields.String,
    'passwd': fields.String,
    'command': fields.String,
})

# class Ssh2_exec(Resource):  # 自定义登录函数
#     # @ns.expect(login_fields, validate=False)
#     @ns.expect(ssh_fields)
#     # 不需要安全登陆信息
#     @ns.doc(security=[])
#     # @api.doc(params={'username': 'Username'})
#     # @api.doc(params={'password': 'Password'})
#     def post(self):
#         return {"message": "用户名或密码错误"}, 401

class Ssh2_exec(Resource):
    @ns.expect(ssh_fields)
    # 不需要安全登陆信息
    @ns.doc(security=[])
    def post(self):
        args = reqparse.RequestParser() \
            .add_argument('ip', type=str, location='json', required=True, help="IP不能为空") \
            .add_argument("port", type=int, location='json', required=True, help="port不能为空") \
            .add_argument("username", type=str, location='json', required=True, help="username不能为空") \
            .add_argument("passwd", type=str, location='json', required=True, help="passwd不能为空") \
            .add_argument("command", type=str, location='json', required=True, help="passwd不能为空") \
            .parse_args()
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(args['ip'], args['port'], args['username'], args['passwd'], timeout=5)
            stdin, stdout, stderr = ssh.exec_command(args['command'])
            return stdout.readlines()
        finally:
            ssh.close()
