from celery import Celery
import redis
import requests
import time
# 我们这里案例使用redis作为broker和backend
app = Celery('demo',
             backend='redis://127.0.0.1:6379/2',
             broker='redis://127.0.0.1:6379/1')


# 创建任务函数
@app.task
def my_task(a, b):
    print("任务函数正在执行....")
    return a + b


@app.task
def task_list_test():
    pool = redis.ConnectionPool()
    r = redis.Redis(connection_pool=pool)
    # 将本任务添加到队列，任务名为task_name_001,状态为false
    r.rpush('task_name_list', "task_name_001")
    r.set('task_name_001', "false")

    # 这里设置任务为访问网络
    print(requests.request('GET', 'http://www.baidu.com').content)
    time.sleep(10)

    # 设置任务状态为完成
    r.set('task_name_001', 'true')

    print('task finish')
