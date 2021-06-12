from __future__ import absolute_import
from flask import Flask, request  # 导入Flask类
from flask_restful import Api, Resource
from app import *
from tasks import *
from bson import json_util, ObjectId
import json
from celery.result import AsyncResult

app = create_app()  # 实例化并命名为app实例
api = Api(app)


# 任务列表管理
class TaskAdmin(Resource):
    def post(self):
        datajson = {
            'name': request.json.get('task_name'),
            'description': request.json.get('task_desc'),
            'ip': request.json.get('task_ip'),
            'port': request.json.get('task_port'),
            'thread_num': request.json.get('task_thread_num')
        }
        # 将数据存到数据库
        my_col.insert_one(datajson)
        # 将任务加入到celery任务队列中
        task = work.delay(datajson['name'])
        # 将任务id存储到数据库中
        my_col.update_one(filter={'name': {'$regex': datajson['name']}}, update={'$set': {'task_id': str(task.id)}})

    def get(self):
        return json_util.dumps(my_col.find())

    def delete(self):
        my_col.delete_many({})


# 任务信息管理
class TaskOp(Resource):
    def get(self):
        name = request.args.get('task_name')
        data = my_col.find_one({'name': name})
        if data:
            result = app_celery.AsyncResult(data['task_id'])
            result.get(on_message=on_raw_message, propagate=False)
            return result.state
        return "ERROR"

    def delete(self):
        name = request.json.get('task_name')
        my_col.delete_one({'name': name})




api.add_resource(TaskAdmin, "/api/admin")
api.add_resource(TaskOp, "/api/task")

if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1", debug=True)  # 调用run方法，设定端口号，启动服务
