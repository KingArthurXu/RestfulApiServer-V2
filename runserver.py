#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'

import logging.config

from App import app

import sys
reload(sys)
sys.setdefaultencoding('utf8')

logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

if __name__ == '__main__':
    log.info('>>>>> Starting server <<<<<')
    import os
    flask_host = os.getenv("FLASK_HOST") if os.getenv("FLASK_HOST") else '0.0.0.0'
    flask_port = os.getenv("FLASK_PORT") if os.getenv("FLASK_PORT") else '5000'
    flask_debug = os.getenv("FLASK_DEBUG") if os.getenv("FLASK_DEBUG") else "True"
    app.run(host=flask_host, port=int(flask_port), debug=bool(flask_debug))

    # flask_ssl_context = os.getenv("FLASK_SSL_CONTEXT") if os.getenv("FLASK_SSL_CONTEXT") else 'None'
    # app.run(ssl_context=flask_ssl_context, host=flask_host, port=int(flask_port), debug=bool(flask_debug))
    # 证书玩法
    # app.run(debug=True, ssl_context=(
    #     "server/server-cert.pem",
    #     "server/server-key.pem")
    # )
