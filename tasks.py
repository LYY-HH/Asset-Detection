from app import *
from bson import ObjectId
import time


# 添加探测任务
@app_celery.task(bind=True, track_started=True)
def work(self, name):
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 50})
    time.sleep(1)
    self.update_state(state="PROGRESS", meta={'progress': 90})
    time.sleep(1)
    data = my_col.find_one({'name': name})


def on_raw_message(body):
    print(body['status'])
