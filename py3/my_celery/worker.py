#! coding:utf-8
from tasks import my_task, task_list_test
import time
import redis

def run_task():
    ret = my_task.delay(520, 520)
    print(ret.result)
    time.sleep(1)
    print(ret.result)

def base_operation():
    # 创建连接，默认数据库参数
    r = redis.Redis()

    # 可以使用连接池
    pool = redis.ConnectionPool()
    r = redis.Redis(connection_pool=pool)
    r.set('name', 'my name')  # 添加
    print(r.get('name'))  # b'my name'

    # 批量操作
    r.mset({"key1": 'value1', "key2": 'value2'})
    print(r.mget(["key1", "key2"]))  # [b'value1', b'value2']

    # String操作
    r.set('t', '测试')
    print((r.get('t').decode('utf-8')))  # 测试

    # hash测试
    dic = {"a1": "aa", "b1": "bb"}
    r.hmset("dic_name", dic)
    print(r.hmget("dic_name", ["a1", "b1"]))  # [b'aa', b'bb']
    print(r.hget("dic_name", "b1"))  # b'bb'

    # list测试
    # 在name对应的list中添加元素，每个新的元素都添加到列表的最左边
    r.lpush("list_name", 2)
    r.lpush("list_name", 3, 4, 5)  # 保存在列表中的顺序为5，4，3，2
    # name对应的list元素的个数
    print(r.llen("list_name"))  # 4
    # 对list中的某一个索引位置重新赋值
    r.lset("list_name", 0, "bbb")  # b'bbb'
    # 移除列表的左侧第一个元素，返回值则是第一个元素
    print(r.lpop("list_name"))
    # 根据索引获取列表内元素
    print(r.lindex("list_name", 1))  # b'3'
    # 删除name对应的list中的指定值
    r.lrem("list_name", value=3, count=0)

    # set测试
    # 给name对应的集合中添加元素,元素不重复
    r.sadd("set_name", "aa")
    r.sadd("set_name", "aa", "bb")

    # 设置过期
    r.setex(name='a', value='b', time=10)  # 设置过期时间（秒）
    print(r.get('a'))  # b'b'
    time.sleep(10)
    print(r.get('a'))  # None, 已经过期了


def run_task_list():
    """
    模拟检测异步任务状态
    :return:
    """
    r = redis.Redis()
    r.delete('task_name_list')
    r.delete('task_name_001')

    r = redis.Redis()

    # 异步执行任务
    task_list_test.delay()
    print(r.get('task_name_001'))  # None
    print(r.lrange("task_name_list", 0, -1))  # []
    time.sleep(20)
    print(r.get('task_name_001'))  # 'true'
    print(r.lrange("task_name_list", 0, -1))  # [b'task_name_001']


if __name__ == '__main__':
    run_task_list()
    # base_operation()
    # print(r.get('add_data'))
    # run_task_add_data()
    # pool = redis.ConnectionPool()
    # r = redis.Redis(connection_pool=pool)
    # print(r.get('add_data'))  # 获取
