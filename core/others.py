# -*- coding: utf-8 -*-
import requests
import json
import time
import exception
import redis


class DadaRedis(object):
    # 类的初始化
    def __init__(self, host, port):
        # 实现StrictRedis的连接池
        self.__redis = redis.StrictRedis(host, port)

    # 获取指定key的Value
    def get(self, key):

        try:
            # 判断是否存在该Key值
            if not self.__redis.exists(key):
                raise core.others.custom_exception.Dada_norediskey_exception(
                    key)
        except core.others.custom_exception.Dada_norediskey_exception as x:
            print '错误概述--->', x
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
        else:
            # 输出Value值
            return self.__redis.get(key)

    def set(self, key, value, extime):
        try:
            if isinstance(key, None) or len(key) == 0:
                raise core.others.custom_exception.Dada_emptykey_exception(key)
        except core.others.custom_exception.Dada_emptykey_exception as x:
            print '错误概述--->', x
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
        else:
            # 输出Value值
            self.__redis.set(key, value, extime)
