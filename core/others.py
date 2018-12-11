# -*- coding: utf-8 -*-
import requests
import json
import time
from exception import EmptyException, RaizeCurrentException
import redis

# 搭搭云微信其他：
# 1，包括Redis设置，Sql设置，Log设置，线程设置。


# 搭搭云Redis类，包含HOST，POST以及登录信息。
# 创建搭搭注册类，意味服务器与username用户创建关联（已实现）
# 初始创建需要输入用户名、密码等信息，Token有效期内，免密关联。（已实现）
# 若用户未续约Token，则关联类自动取消（已实现）
# 若用户登录Cookie被清除，则关联类自动取消（未实现）
# 若用户修改用户名，则关联类自动取消（未实现）
# 若用户未登录时间超过180天，则关联自动取消（已实现）


class DadaRedis(object):
    # 类的初始化
    def __init__(self, host, port, login):
        # 实现StrictRedis的连接池
        self.__redis = redis.StrictRedis(host, port)
        self.loginInstance = login

    # 获取指定key的Value，需要引入login类
    def get(self, key):

        try:
            # 判断是否存在该Key值
            if not self.__redis.exists(key):
                raise EmptyException(
                    'redis_key_empty')
        except EmptyException as x:
            output = RaizeCurrentException(x, self.loginInstance)
            output.output()
        finally:
            # 输出Value值
            return self.__redis.get(key)

    # 给指定key设置Value，需要引入login类
    def set(self, key, value, extime):
        try:
            if len(key) == 0:
                raise EmptyException('param_empty')
        except EmptyException as x:
            output = RaizeCurrentException(x, self.loginInstance)
            output.output()
        else:
            # 输出Value值
            self.__redis.set(key, value, extime)
