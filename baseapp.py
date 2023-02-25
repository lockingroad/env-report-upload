from flask import Flask, request
from flask_restful import Api
from model.models import db
from flask_rest_paginate import Pagination

# 初始化
app = Flask(__name__, template_folder='./templates')
api = Api(app)
app.config.from_pyfile('config.py')

# 数据库配置
db.app = app
db.init_app(app)
pagination = Pagination(app, db)