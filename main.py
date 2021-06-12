from flask import Flask, request  # 导入Flask类
from flask_restful import Api, Resource
from app import *
from tasks import *
from bson import json_util, ObjectId
import json
from celery.result import AsyncResult

app = create_app()  # 实例化并命名为app实例
api = Api(app)


class CreateTask(Resource):
    def post(self):
        datajson = {
            'name': request.json.get('task_name'),
            'description': request.json.get('task_desc'),
            'ip': request.json.get('task_ip'),
            'port': request.json.get('task_port'),
            'thread_num': request.json.get('task_thread_num')
        }

        # 将数据存到数据库并获取对应数据的task_id
        result = my_col.insert_one(datajson)
        task_id = result.inserted_id
        # 将任务加入到celery任务队列中 输出参数为 task_id
        data = work.delay(str(task_id))
        my_col.update_one(filter={'name': {'$regex': datajson['name']}}, update={'$set': {'task_id': str(data.id)}})


# 获取所有任务队列
class TaskList(Resource):
    def get(self):
        return json_util.dumps(my_col.find())


# 获取特定任务状态
class TaskInquire(Resource):
    def get(self):
        name = request.args.get('task_name')
        data = my_col.find_one({'name': name})
        result = AsyncResult(data['task_id'])
        print(result)
        return json.dumps(result.get(propagate=False))


# 终止任务
class TaskDelete(Resource):
    def delete(self):
        id = request.json.get('task_id')
        data = my_col.find_one({'_id': ObjectId(id)})


api.add_resource(CreateTask, "/api/create_task")
api.add_resource(TaskList, "/api/task/list")
api.add_resource(TaskInquire, "/api/task/inquire")

if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1", debug=True)  # 调用run方法，设定端口号，启动服务
