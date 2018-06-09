#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'

import logging
import traceback

from flask import Blueprint
from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound
from App import app


log = logging.getLogger(__name__)

# api_blueprint = Blueprint('BaaS', __name__, url_prefix='/api')
api_blueprint = Blueprint('BaaS', __name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    app=api_blueprint,
    default='BaaS API',
    default_label='BaaS API',
    authorizations=authorizations,
    validate = False,
    version='1.0.0',
    title='NetBackup BaaS API',
    # description='''<p>This is an example developed to show how can we configure a
    #     REST API using NetBackup Baas API and Swagger for documenting the API</p>
    description='''<p><a class="btn btn-primary" href="/admin/">管理接口</a></p>''',
    # contact='qingyu.xu@veritas.com',
    # contact_url='http://www.veritas.com',
)


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)
    if not app.config.get("FLASK_DEBUG"):
        return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404



from App.endpoints.auth import ns_auth
# from App.restapi.endpoints.bpimagelist import ns_bpimagelist
# from App.restapi.endpoints.bpdbjobs import ns_bpdbjobs
from App.endpoints.nbuapi import ns_nbu
api.add_namespace(ns_auth)
# api.add_namespace(ns_bpimagelist)
# api.add_namespace(ns_bpdbjobs)
api.add_namespace(ns_nbu)

