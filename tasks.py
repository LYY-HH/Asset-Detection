from app import *
from bson import ObjectId


@celery.task
def work(task_id):
    data = my_col.find_one({'_id': ObjectId(task_id)})
    data['status'] = 'running'
