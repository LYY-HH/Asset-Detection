from flask import Flask, request  # 导入Flask类
from app import *
from tasks import work
from bson import json_util
import json


app = create_app()  # 实例化并命名为app实例
# 删除所有数据
my_col.delete_many({})


# 创建任务
@app.route('/api/create_task', methods=['POST'])
def create_task():
    if request.method == 'POST':
        #  缺少参数校验，方法一使用 flask_restful 中的 reqparse;
        #  方法二，使用 WTforms，参考链接: https://zhuanlan.zhihu.com/p/336091060
        #                                                                       ---wangyx
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
@app.route('/api/task/list', methods=['GET'])
def task_list():
    if request.method == 'GET':
        return json_util.dumps(my_col.find())


if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1", debug=True)  # 调用run方法，设定端口号，启动服务
