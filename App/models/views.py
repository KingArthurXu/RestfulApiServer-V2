#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'

# 后台管理
# from flask_admin import Admin, BaseView, expose
# from flask_admin.contrib.sqla import ModelView
# admin = Admin(app, name=u'BaaS AP Server 后台管理系统', template_mode='bootstrap3')
# admin.add_view(ModelView(User, db.session,name=u'用户管理'))
# admin.add_view(ModelView(Role, db.session,name=u'权限管理'))
# # admin.add_view(ModelView(roles_users, db.session,name=u'用户权限管理'))

from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, form
from flask_admin.contrib import sqla
import os
from flask_admin import BaseView, expose
from wtforms import TextField
from flask import redirect, url_for, request
from flask_login import current_user
from flask_security import login_user, logout_user
from db import User
from App import db, app
from passlib.handlers.django import django_pbkdf2_sha256
from flask import flash


class MyPassField(TextField):
    def process_data(self, value):
        self.data = 'MyPassField'  # even if password is already set, don't show hash here
        # or else it will be double-hashed on save
        # self.orig_hash = value

    def process_fromdata(self, valuelist):
        value = ''
        if valuelist:
            value = valuelist[0]
        # if value:
        #     self.data = generate_password_hash(value)
        # else:
        #     self.data = self.orig_hash


class UserView(ModelView):
    # def _user_formatter(view, context, model, name):
    #     # if model.url:
    #     if name == "password":
    #        # markupstring = "<a href='%s'>%s</a>" % ('AA', 'BB')
    #        # return Markup(markupstring)
    #         return "please change me"
    #     else:
    #        return ""
    #
    # column_formatters = {
    #     'password': _user_formatter
    # }
    #
    #
    #
    form_overrides = dict(
        password=MyPassField,
    )
    # form_widget_args = dict(
    #     # password=dict(
    #     #     placeholder='Enter new password here to change password',
    #     # ),
    #     password={'description': {
    #         'rows': 20,
    #         'style':'width: 1000px;'
    #     },
    # )

    def _get_field_value(self, model, name):
        if name == 'password':
            return "********"
        else:
            # 调用上级函数的方法
            return super(UserView, self)._get_field_value(model, name)

    # 在Edit Tab中有效
    def on_form_prefill(self, form, id):
        form.password.data = 'changeme'

    def is_accessible(self):
        return current_user.is_authenticated

    def on_model_change(self, form, User, is_created):
        User.password = django_pbkdf2_sha256.encrypt(form.password.data)

    can_view_details = True
    column_list = ['username', 'password', 'active', 'roles']
    # column_list = ['username', 'password', 'active']
    column_default_sort = ('username', False)
    column_filters = [
        'username',
        'active',
    ]
    column_details_list = [
        'username', 'password', 'active', 'roles'
    ]
    form_columns = [
        'username', 'password', 'active', 'roles',
    ]


class RoleView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated
    column_list = ['name', 'description', 'user']
    form_columns = ['name', 'description', 'user']
    # column_list = ['name', 'description']
    # form_columns = ['name', 'description']


# class UserRoleView(BaseView):
#     def is_accessible(self):
#         return current_user.is_authenticated

# # Create custom admin view
# class MyAdminView(BaseView):
#     @expose('/')
#     def index(self):
#         return self.render('myadmin.html')


# Logout 界面
class MyLogoutView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated
    @expose('/')
    def Logout(self):
        if current_user.is_authenticated:
            logout_user()
            flash(u'退出登录', 'warning')
        return redirect(url_for("admin.index"))


# 登录界面
class MyLoginView(BaseView):
    def is_accessible(self):
        return not current_user.is_authenticated

    @expose('/',('GET','POST'))
    def Login(self):
        if not current_user.is_authenticated:
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                user = User.authenticate(username, password)
                if user:
                    login_user(user=user)
                    flash(u'成功登录')
                    return redirect(url_for("admin.index"))
                else:
                    # flash  a message
                    return self.render('admin_login.html')
            else:
                return self.render('admin_login.html')
        else:
            return redirect(url_for("admin.index"))


def prefix_name(obj, file_data):
    import os
    parts = os.path.splitext(file_data.filename)
    from werkzeug.utils import secure_filename
    return secure_filename('file-%s%s' % parts)


class ShellFileView(sqla.ModelView):

    column_display_pk = True # optional, but I like to see the IDs in the list

    # 控制该试图是否可见
    def is_accessible(self):
        return current_user.is_authenticated
        # return current_app.login.current_user.is_authenticated()

    column_list = ['id', 'name', 'path']
    form_columns = ['name', 'path']

    # Override form field to use Flask-Admin FileUploadField
    form_overrides = {
        'path': form.FileUploadField
    }

    # Pass additional parameters to 'path' to FileUploadField constructor
    form_args = {
        'path': {
            'label': 'File',
            'base_path': os.path.join(app.root_path, app.config['UPLOAD_DIR']),
            'allow_overwrite': True,
            'permission': 0o766
        }
    }


class ShellParamView(sqla.ModelView):
    # 控制该试图是否可见
    def is_accessible(self):
        return current_user.is_authenticated
        # return current_app.login.current_user.is_authenticated()

    # optional, but I like to see the IDs in the list
    column_display_pk = True
    column_hide_backrefs = False
    can_view_details = True
    # column_list = ["shellfile_id", 'param_order', 'param_name', 'default_value']
    # form_columns = ["shellfile_id", 'param_order', 'param_name', 'default_value']
    column_filters = ["shellfile_id"]
    form_choices = {
        'param_order': [
            ('1', u'第一参数'),
            ('2', u'第二参数'),
            ('3', u'第三参数'),
            ('4', u'第四参数'),
            ('5', u'第五参数'),
            ('6', u'第六参数'),
        ]
    }

    # def _get_field_value(self, model, name):
    #     if name == 'password':
    #         return "********"
    #     else:
    #         # 调用上级函数的方法
    #         return super(UserView, self)._get_field_value(model, name)
    # # 在Edit Tab中有效
    # def on_form_prefill(self, form, id):
    #     form.password.data = 'changeme'

    # 提交的时候检查参数配置是否按顺序
    # # from flask_sqlalchemy import
    # def on_model_change(self, form, ShellParam, is_created):
    #     # print ShellParam.param_order
    #     # print is_created
    #     if ShellParam.param_order <> 1:
    #         print is_created
    #         # raise u"清按"
    #
    #     # if end date before start date or end date in the past, flag them invalid
    #     if (form.scheduled_end.data <= form.scheduled_start.data or
    #         form.scheduled_end.data <= datetime.datetime.utcnow()):
    #         raise validators.ValidationError('Invalid schedule start and end time!')
    #     else:
    #         super().on_model_change(form, model, is_created)

    from flask import flash
    # def validate_form(self, form):
    #     """ Custom validation code that checks dates """
    #     # a = form.param_order.data
    #     if not form.param_order.data:
    #         # flash(u"请按顺序开始配置参数")
    #         return False
    #         # flash(u"请按顺序开始配置参数")
    #     else:
    #         # flash(form.shellfile_id.id)
    #         # return False
    #         sp_list = ShellParam.query.filter(ShellParam.shellfile_id == form.ShellFile.data.id).all()
    #         max_po = 0
    #         for sp in sp_list:
    #             if sp.param_order > max_po:
    #                 max_po = sp.param_order
    #         # flash(form.param_order.data)
    #         # flash(form.param_order.data)
    #         if int(form.param_order.data) == (max_po+1):
    #             return True
    #         else:
    #             form.param_order.data = unicode(max_po+1)
    #             flash(u"参数需要按顺序配置，需要配置第%s个参数" % unicode(max_po+1), "error")
    #
    #             return False
    #     return super(ShellParamView, self).validate_form(form)

    # def on_model_change(self, form, ShellParam, is_created):
        # if not is_created:
        #     raise "aaasdfasdf"

