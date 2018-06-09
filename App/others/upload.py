#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Arthur Xu'

import logging

from App import app
from flask import request, redirect, url_for, render_template_string
from flask import Blueprint
from werkzeug.utils import secure_filename
import os

log = logging.getLogger(__name__)

site_blueprint = Blueprint('site', __name__, url_prefix='/upload')

upload_html = u'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>Shell文件上传</h1>
    <form action="" enctype='multipart/form-data' method='POST'>
        <input type="file" name="file">
        <input type="submit" value="上传">
    </form>
</body>
</html>
'''


@site_blueprint.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        # basepath = os.path.dirname(__file__)  # 当前文件所在路径
        # basepath = os.path.dirname(app.)
        upload_path = os.path.join(app.root_path, app.config['UPLOAD_DIR'], secure_filename(f.filename))  #注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        return redirect(url_for('site.upload'))
    return render_template_string(upload_html)

