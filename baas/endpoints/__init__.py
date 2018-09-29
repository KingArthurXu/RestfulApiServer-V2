#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'
import traceback
from flask import Blueprint
from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound
from manage import app
from auth import *
from bpdbjobs import *
from popen import *
from nbuapi import *
from decorators import *


import logging
logging.basicConfig()


# api_blueprint = Blueprint('baas', __name__, url_prefix='/baas')
api_blueprint = Blueprint('baas', __name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    # 'content_type': {
    #     'type': 'content_type',
    #     'in': 'header',
    #     'name': 'content-type'
    # },
    #content-type: application/vnd.netbackup+json;version=1.0'
}

api = Api(
    app=api_blueprint,
    default='baas API',
    default_label='baas API',
    authorizations=authorizations,
    validate=False,
    version='1.0.0',
    title='NetBackup baas API',
    # description='''<p>This is an example developed to show how can we configure a
    #     REST API using NetBackup Baas API and Swagger for documenting the API</p>
    # description='''<p><a class="btn btn-primary" href="/admin/">管理接口</a></p>''',
    # contact='qingyu.xu@veritas.com',
    # contact_url='http://www.veritas.com',
)

# Swagger UI document
# baas = Api(app, doc=False)
# Swagger UI Configuration
app.config.SWAGGER_UI_DOC_EXPANSION = 'list'


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    logging.exception(message)
    if not app.config.get("FLASK_DEBUG"):
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    logging.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404


from baas.endpoints.auth import ns_auth
from baas.endpoints.nbuapi import ns_nbu
# from baas.restapi.endpoints.bpimagelist import ns_bpimagelist
# from baas.restapi.endpoints.bpdbjobs import ns_bpdbjobs

api.add_namespace(ns_auth)
api.add_namespace(ns_nbu)
# baas.add_namespace(ns_bpimagelist)
# baas.add_namespace(ns_bpdbjobs)