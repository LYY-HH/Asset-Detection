from __future__ import absolute_import
from flask import Flask, request  # 导入Flask类
from flask_restful import Api, Resource
from app import *
from tasks import *
from bson import json_util, ObjectId
import json
from celery.result import AsyncResult
from celery.app.control import Control

app = create_app()  # 实例化并命名为app实例
api = Api(app)
celery_control = Control(app_celery)


@app.route("/")
def hello():
    return "Hello World!"


# 任务列表管理
class TaskList(Resource):
    # 创建任务
    def post(self):
        datajson = {
            'name': request.values.get('task_name'),
            'description': request.values.get('task_desc'),
            'ip': request.values.get('task_ip'),
            'port': request.values.get('task_port'),
            'thread_num': request.values.get('task_thread_num')
        }
        # 将数据存到数据库
        my_col.insert_one(datajson)

    # 返回任务列表
    def get(self):
        return json_util.dumps(my_col.find())

    # 清空任务列表
    def delete(self):
        my_col.delete_many({})


# 任务状态管理
class TaskState(Resource):
    # 获取任务状态
    def get(self):
        name = request.args.get('task_name')
        data = my_col.find_one({'name': name})
        if 'state' in data:
            task_id = data['task_id']
            state = AsyncResult(id=str(task_id), app=app_celery).state
            my_col.update_one(filter={'name': {'$regex': name}}, update={'$set': {'state': str(state)}})
            return state
        return "ERROR"

    # 终止任务
    def delete(self):
        name = request.values.get('task_name')
        data = my_col.find_one({'name': name})
        if 'state' in data:
            task_id = data['task_id']
            celery_control.revoke(str(task_id), terminate=True)
            state = AsyncResult(id=str(task_id), app=app_celery).state
            my_col.update_one(filter={'name': {'$regex': name}}, update={'$set': {'state': str(state)}})
            return "OK"
        return "ERROR"

    # 开始任务
    def post(self):
        name = request.values.get('task_name')
        data = my_col.find_one({'name': name})
        if data:
            # 将任务加入到celery任务队列中
            task = work.delay(name)
            state = AsyncResult(id=str(task.id), app=app_celery).state
            # 将任务id存储到数据库中
            my_col.update_one(filter={'name': {'$regex': name}}, update={'$set': {'task_id': str(task.id)}})
            my_col.update_one(filter={'name': {'$regex': name}}, update={'$set': {'state': str(state)}})
            return "OK"
        return "ERROR"



api.add_resource(TaskList, "/api/task")
api.add_resource(TaskState, "/api/control")

if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1", debug=True)  # 调用run方法，设定端口号，启动服务
