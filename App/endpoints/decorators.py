#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'


from werkzeug.wrappers import Request as RequestBase, Response as ResponseBase
from functools import wraps
from werkzeug.local import LocalProxy
from flask import Response, _request_ctx_stack, abort, current_app, redirect, \
    request, url_for, g, session
from flask_principal import Identity, Permission, RoleNeed, identity_changed

# Convenient references
_security = LocalProxy(lambda: current_app.extensions['security'])


def auth_token_required(fn):
    """Decorator that protects endpoints using token authentication. The token
    should be added to the request by the client by using a query string
    variable with a name equal to the configuration value of
    `SECURITY_TOKEN_AUTHENTICATION_KEY` or in a request header named that of
    the configuration value of `SECURITY_TOKEN_AUTHENTICATION_HEADER`
    """
    @wraps(fn)
    def decorated(*args, **kwargs):
        if _check_token():
            return fn(*args, **kwargs)
        else:
            # return _get_unauthorized_response()
            return {"message": "认证失败"}, 201
    return decorated


def _check_token():
    user = _security.login_manager.request_callback(request)

    if user and user.is_authenticated:
        # app = current_app._get_current_object()
        app = current_app
        _request_ctx_stack.top.user = user
        # LocalStack.top.user = user
        identity_changed.send(app, identity=Identity(user.id))
        return True
    return False


def roles_required(*roles):
    """Decorator which specifies that a user must have all the specified roles.
    Example::

        @app.route('/dashboard')
        @roles_required('admin', 'editor')
        def dashboard():
            return 'Dashboard'

    The current user must have both the `admin` role and `editor` role in order
    to view the page.

    :param args: The required roles.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            perms = [Permission(RoleNeed(role)) for role in roles]
            for perm in perms:
                if not perm.can():
                        return {"message": "无权限"}, 201
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

