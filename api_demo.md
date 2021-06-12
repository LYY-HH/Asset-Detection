### 任务探测接口

#### /api/admin

接口描述：任务列表管理

| 请求模式 | 参数                                                         | 功能描述                                           |
| -------- | ------------------------------------------------------------ | -------------------------------------------------- |
| POST     | task_name(string, required)<br>task_desc(string,required)<br>task_ip(string, required)<br>task_port(string, required)<br>task_threadnum(string) | 创建任务: 任务名称、任务描述、ip地址、端口、进程数 |
| DELETE   | /                                                            | 清空任务列表                                       |
| GET      | /                                                            | 获取任务列表                                       |

#### /api/task

接口描述：任务信息管理

| 请求模式 | 参数                   | 功能描述         |
| -------- | ---------------------- | ---------------- |
| GET      | task_name(str, required) | 获取特定任务状态 |
| DELETE | task_name(str, required) | 终止/删除任务 |
| POST | task_name(str, required) | 开始任务 |

#### /api/task/pause

接口描述：暂停任务

| 请求模式 | 参数                   | 功能描述 |
| -------- | ---------------------- | -------- |
| POST     | task_name(str, required) | 暂停任务 |
