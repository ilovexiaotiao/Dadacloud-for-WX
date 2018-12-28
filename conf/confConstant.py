# -*- coding: utf-8 -*-
import time


# 公共函数时间常量


class ConstantTime(object):
    # 类的初始化,type=0,则为LOGIN类时间常量，其他情况，为非LOGIN类常量,需要补全expire_time
    def __init__(self, second, types=0, expire_time_login=time.localtime(
            0)):
        self.second = second
        self.types = types
        self.expire_time_login = expire_time_login

    # Time类型当前时间

    def now_time(self):
        return time.localtime(
            time.time())

    # 字符串类型当前时间

    def now_time_string(self):
        return time.strftime(
            '%Y-%m-%d %H:%M:%S', self.now_time())

    # Time类型失效时间,
    def expire_time(self):
        if self.types > 0:
            return min(time.localtime(
                time.time() + int(self.second)), self.expire_time_login)
        else:
            return time.localtime(
                time.time() + int(self.second))

    # 字符串类型失效时间
    def expire_time_string(self):
        return time.strftime(
            '%Y-%m-%d %H:%M:%S', self.expire_time())

    # 判断当前是否过了有效期

    def get_expire(self):
        # 获取当前时间
        now = self.now_time()
        # 判断返回结果中是否有错误提示
        return now > self.expire_time()
