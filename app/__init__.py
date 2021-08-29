from flask import Flask
from celery import Celery
import pymongo
import mongoengine

# 连接数据库
my_client = pymongo.MongoClient("mongodb://localhost:27017/")
# 连接db
my_db = my_client["detection"]
# 连接集合
my_col = my_db["tasks"]

app_celery = Celery(__name__, broker='redis://localhost:6379//'
                    , backend='redis://')


def create_app():
    app = Flask(__name__,  template_folder='../templates')
    return app
