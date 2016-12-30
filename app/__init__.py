#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 注意：必须先实例化app才能导入依赖app的views和models。
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import models, views
