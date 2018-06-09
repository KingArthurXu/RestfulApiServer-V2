#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'

from App import db, app
# 添加部分用户表的方法
from flask_security import UserMixin, RoleMixin
from passlib.handlers.django import django_pbkdf2_sha256
from flask import flash
import os

# 文件监听
from sqlalchemy.event import listens_for


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    addresses = db.relationship('Address', backref='person', lazy=True)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=False)


user_to_role = db.Table('user_to_role',  # 用户权限中间表
                        db.Column('id', db.Integer(), primary_key=True, autoincrement=True),
                        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


#
# 从多个对象创建复合对象
#
class Role(db.Model, RoleMixin):  # 权限表
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # 定义可用多个形式
    # def __init__(**kwargs):
    #
    # def __init__(self, name, description):
    #     self.name = name
    #     self.description = description
    # def __init__(self, **kwargs):
    #     for key, value in kwargs.items():
    #         setattr(self, key, value)

    def __str__(self):
        return '<Role %r>' % self.name

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):  # 用户表
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(11), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    roles = db.relationship('Role', secondary=user_to_role, backref=db.backref('user', lazy='select'))

    def __init__(self, ** kwargs):
        for key, value in kwargs.items():
            if key == 'password':
                setattr(self, key, django_pbkdf2_sha256.encrypt(value))
            else:
                setattr(self, key, value)

    # def __init__(self, username=None, password=None, active=True):
    #     self.username = username
    #     if password:
    #         self.password = django_pbkdf2_sha256.encrypt(password)
    #     self.active = True

    def __str__(self):
        return '<User %r>' % self.username

    # 可以打印用户信息
    def __repr__(self):
        return '<User %r>' % self.username

    # 可以不设置，直接setter
    # @property
    # def password(self):
    #     return self.password
    #
    # @password.setter
    # def password(self, password):
    #     self.password_hash = django_pbkdf2_sha256.encrypt(password)

    @staticmethod
    def authenticate(username, password):
        user = User.query.filter(User.username == username).first()
        if user and django_pbkdf2_sha256.verify(password, user.password):  # 自行选择密码算法
            return user


# Shell脚本数据库
class ShellFile(db.Model):
    __tablename__ = 'shellfile'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(64))
    path = db.Column(db.Unicode(128))
    params = db.relationship('ShellParam', backref='ShellFile', lazy=True)
    # def __unicode__(self):
    #     return self.name

    def __str__(self):
        return '<Shell#%d %s>' % (self.id, self.name)

    def __repr__(self):
        return '<Shell#%d %s>' % (self.id, self.name)


# 在删除记录后删除文件
@listens_for(ShellFile, 'after_delete')
def del_file(mapper, connection, target):
    if target.path:
        try:
            # os.path.join(app.rootpath, 'static\uploads', secure_filename(f.filename))
            os.remove(os.path.join(os.path.dirname(__file__), app.config['UPLOAD_DIR'], target.path))
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass


# 在删除记录后删除文件
@listens_for(ShellFile, 'after_delete')
def del_file(mapper, connection, target):
    if target.path:
        try:
            # os.path.join(app.rootpath, 'static\uploads', secure_filename(f.filename))
            os.remove(os.path.join(os.path.dirname(__file__), app.config['UPLOAD_DIR'], target.path))
        except OSError:
            # Don't care if was not deleted because it does not exist
            pass


# 在新增加文件后自动配置文件参数
@listens_for(ShellFile, 'after_insert')
def isnert_file(mapper, connection, target):
    if target.path:
        try:
            from App.endpoints.nbuapi import auto_config_shell_params
            auto_config_shell_params(target.path)
        except OSError:
            pass


class ShellParam(db.Model):
    __tablename__ = 'shellparam'
    id = db.Column(db.Integer, primary_key=True)
    param_order = db.Column(db.Integer, nullable=False)
    param_name = db.Column(db.String(120), nullable=False)
    required = db.Column(db.Boolean(), default=True, nullable=False)
    help = db.Column(db.String(120), nullable=False)
    default_value = db.Column(db.String(120), nullable=False)
    shellfile_id = db.Column(db.Integer, db.ForeignKey('shellfile.id'), nullable=False)

    def __unicode__(self):
        return self.param_name

    def __str__(self):
        return self.param_name

    def __repr__(self):
        return self.param_name
