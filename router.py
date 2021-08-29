# -*- coding:utf-8 -*-
# @FileName  :router.py
# @Time      :2021/8/29 15:20

from flask_restful import Api
from main import app, TaskList, TaskState
from login import blue_view_login

app.register_blueprint(blue_view_login)
api = Api(app)

api.add_resource(TaskList, "/api/task")
api.add_resource(TaskState, "/api/control")
