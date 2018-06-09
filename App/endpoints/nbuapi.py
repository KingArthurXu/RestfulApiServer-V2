#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'

import logging
import os
import shlex
import subprocess
from collections import namedtuple

from flask_restplus import Resource, fields, Namespace, reqparse

from App import app
from App.models.db import ShellFile, ShellParam, db
from App.endpoints import NoResultFound
import collections


log = logging.getLogger(__name__)

ns_nbu = Namespace('netbackup', description='NetBackup 全部接口')


def get_shell_output(apiname):
    with open(os.devnull, 'w') as FNULL:
        params = ['C:\\Users\\Qingyu.Xu\\PycharmProjects\\RestfulApiServer\\App\\static\\uploads\\bp.bat']
        try:
            logging.info("Start execute command")
            child=subprocess.Popen(params, stdout=subprocess.PIPE, stderr=FNULL)
            out = child.communicate()[0].splitlines()
            returncode = child.returncode
            NT = namedtuple('FieldHead',shlex.split(out[0]))
            data_list=[]
            for line in out[1:-2]:
                if line:
                    nt = NT(*(shlex.split(line)))
                    data_list.append(nt._asdict())
            result = {'data': data_list, 'code':out[-2], 'message':out[-1]}
            return {"result": result, "returncode": returncode}, 200
        except subprocess.CalledProcessError:
            logging.warn("Failed to execute {0}".format(params))
            return {"result": "", "returncode": -1}, 400


def auto_config_shell_params(apiname):
    shellfile = ShellFile.query.filter(ShellFile.name == apiname).first()
    if not shellfile:
        return {"message": "API not found", "code": -1}, 400
    qry = ShellParam.query.filter(ShellParam.shellfile_id == shellfile.id)
    sp_list = qry.order_by(db.asc(ShellParam.param_order)).all()
    for item in sp_list:
        db.session.delete(item)

    # 构建shell文件名
    script_full_name = os.path.join(app.root_path, app.config['UPLOAD_DIR'], shellfile.name)
    # 自动解析shell参数
    col_param = collections.namedtuple('Parameters', 'PARAM Name Default Required Help')

    shell_lines = bp_file = open(script_full_name, "r").readlines()
    int_order = 1
    params = []
    for line in shell_lines:
        # 自动配置parameter 关键字
        if line[0:6] == '#PARAM' or line[0:8] == '::#PARAM':
            shell_param = col_param(*(shlex.split(line)))
            # print (shell_param._asdict())
            # print shell_param.Name
            new_param = ShellParam(param_order=int_order,
                                   param_name=shell_param.Name,
                                   required=bool(shell_param.Required),
                                   help=shell_param.Help,
                                   default_value=shell_param.Default,
                                   shellfile_id = shellfile.id)

            int_order = int_order + 1
            db.session.add(new_param)
            params.append(shell_param._asdict())
    return params
    # if not sp_list:
    #     return {"message": "API not found", "code": -1}, 400
    # pass


def get_db_shell_output(apiname):
    shellfile = ShellFile.query.filter(ShellFile.name == apiname).first()
    if not shellfile:
        return {"message": "API not found", "code": -1}, 400
    qry = ShellParam.query.filter(ShellParam.shellfile_id == shellfile.id)
    sp_list = qry.order_by(db.asc(ShellParam.param_order)).all()

    # raise NoResultFound

    with open(os.devnull, 'w') as FNULL:
        logging.info("Start execute command")

        # 构建运行命令
        script_full_name = os.path.join(app.root_path, app.config['UPLOAD_DIR'], shellfile.name)
        params = [script_full_name]

        # 取参数个数
        # total_param_order = sp_list.query(db.func.max(ShellParam.param_order)).first()
        # sp_list = sp_list.query.order_by(db.asc(ShellParam.param_order))
        # max_logins = db.session.query(db.func.max(User.numLogins)).scalar()
        # users = db.session.query(User).filter(User.numLogins == max_logins).all()
        # sub = db.session.query(db.func.max(User.numLogins).label('ml')).subquery()
        # users = db.session.query(User).join(sub, sub.c.ml == User.numLogins).all()

        # for shell_param in sp_list:
        #     params.append(shell_param.param_name)
        #
        # return {"result": params, "returncode": 999}, 200

        # 分析JSON 参数
        request_parser = reqparse.RequestParser()
        for sp in sp_list:
            request_parser.add_argument(sp.param_name, type=str, location='json',
                              required=sp.required, help=sp.help)
        args = request_parser.parse_args()
        # args['username']
        # print args['host']
        for shell_param in sp_list:
            name = args[shell_param.param_name]
            # shell_param.param_name
            params.append(name)

        # return {"result": params, "returncode": 999}, 200
        try:
            child = subprocess.Popen(params, stdout=subprocess.PIPE, stderr=FNULL)
            out = child.communicate()[0].splitlines()
            returncode = child.returncode
            NT = namedtuple('FieldHead', shlex.split(out[0]))
            data_list = []
            for line in out[1:-2]:
                if line:
                    nt = NT(*(shlex.split(line)))
                    data_list.append(nt._asdict())
            result = {'data': data_list, 'code': out[-2], 'message': out[-1]}
            return {"api": result, "code": returncode}, 200
        except:
            logging.warn("Failed to execute {0}".format(params))
            return {"message": "Execute shell failed!", "code": -1}, 400


param_fields = ns_nbu.model('param', {
        'host': fields.String,
        'port': fields.String,
    })

option_param_fields = ns_nbu.model('param_option', {
        'config': fields.Boolean,
        'show': fields.Boolean,
    })


@ns_nbu.route('/bp')
class Bpsample(Resource):
    @ns_nbu.expect(param_fields)
    def post(self):
        u"""
        测试接口使用
        ```
        {
          "host": "192.168.1.1",
          "port": "8080"
        }
        ```
        测试接口使用
        """
        # test=url_for('NetbackupApi')+'/bp.bat'
        # print url_for('BaaS.netbackup_NetbackupApi')
        # redirect('/netbackup/api/bp.bat')
        return get_db_shell_output("bp.bat")

# from App.endpoints import api
# model = api.model('Model', {
#         'param_name': fields.String,
#     })

#
# 需要Token的API
@ns_nbu.route('/api/<string:apiname>')
class NetbackupApi(Resource):

    # @auth_token_required
    @ns_nbu.expect(param_fields)
    def post(self, apiname):
        u"""
        通用 NetBackup API接口，可进入后台配置
        ```
        测试用
        ```        
        """
        return get_db_shell_output(apiname)
        # return get_shell_output("TEST")

    @ns_nbu.expect(option_param_fields)
    # @api.marshal_with(model, envelope='resource')
    def patch(self, apiname):
        u"""
        自动配置脚本参数
        ```
         
        ```        
        """
        sp_list = auto_config_shell_params(apiname)
        db.session.commit()
        return {"message": "自动配置参数成功!", "data": sp_list}, 200

if __name__ == "__main__":
    auto_config_shell_params('bp.bat')