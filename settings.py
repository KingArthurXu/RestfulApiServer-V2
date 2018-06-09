#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'
# Flask
DEBUG = True

# Database
SQLALCHEMY_DATABASE_URI = 'sqlite:///sql.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Flask-Security
SECRET_KEY = 'my_secret_key'
SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'
WTF_CSRF_ENABLED = False
SECURITY_TOKEN_MAX_AGE = 86400
SECURITY_UNAUTHORIZED_VIEW = '/'
#
UPLOAD_DIR = 'static/uploads'

# flask_restplus
ERROR_404_HELP = False