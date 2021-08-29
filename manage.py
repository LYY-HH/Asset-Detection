# -*- coding:utf-8 -*-
# @FileName  :manage.py
# @Time      :2021/8/29 15:10


from router import app

if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1", debug=True)  # 调用run方法，设定端口号，启动服务