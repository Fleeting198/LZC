# coding:utf-8
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_admin import Admin

# 注意：必须先实例化app才能导入依赖app的views和models。
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
Bootstrap(app)
admin = Admin(app)

from app import models, views
