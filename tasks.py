from app import *
from bson import ObjectId


# 添加探测任务
@celery.task
def work(task_id):
    data = my_col.find_one({'_id': ObjectId(task_id)})
