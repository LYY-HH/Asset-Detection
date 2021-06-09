from flask import Flask, request  # 导入Flask类
from flask_restful import Api, Resource
from app import *
from tasks import work
from bson import json_util
import json


app = create_app()  # 实例化并命名为app实例
api = Api(app)
# 删除所有数据
my_col.delete_many({})


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
        datajson['task_id'] = task_id
        # 将任务加入到celery任务队列中 输出参数为 task_id
        work.delay(str(task_id))


# 获取所有任务队列
class TaskList(Resource):
    def get(self):
        return json_util.dumps(my_col.find())


api.add_resource(CreateTask, "/api/create_task")
api.add_resource(TaskList, "/api/task/list")


if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1", debug=True)  # 调用run方法，设定端口号，启动服务
