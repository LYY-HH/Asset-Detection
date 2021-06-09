### 任务探测接口

#### /api/create_task

接口描述：创建任务

| 请求模式 | 参数                                                         | 功能描述                                           |
| -------- | ------------------------------------------------------------ | -------------------------------------------------- |
| POST     | task_name(string, required)<br>task_desc(string,required)<br>task_ip(string, required)<br>task_port(string, required)<br>task_threadnum(string) | 创建任务: 任务名称、任务描述、ip地址、端口、进程数 |

#### /api/task/list

接口描述：获取任务列表

| 请求模式 | 参数 | 功能描述     |
| -------- | ---- | ------------ |
| GET      | /    | 获取任务列表 |

#### /api/task/inquire

| 请求模式 | 参数                   | 功能描述         |
| -------- | ---------------------- | ---------------- |
| GET      | task_id(int, required) | 获取特定任务状态 |

#### /api/task/pause

接口描述：暂停任务

| 请求模式 | 参数                   | 功能描述 |
| -------- | ---------------------- | -------- |
| POST     | task_id(int, required) | 暂停任务 |

#### /api/task/start

| 请求模式 | 参数                   | 功能描述 |
| -------- | ---------------------- | -------- |
| POST     | task_id(int, required) | 开始任务 |

#### api/task/delete

| 请求模式 | 参数                   | 功能描述      |
| -------- | ---------------------- | ------------- |
| DELETE   | task_id(int, required) | 终止/删除任务 |
