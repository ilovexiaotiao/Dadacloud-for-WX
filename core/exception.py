# -*- coding: utf-8 -*-
import requests
import json
import time
import sys
from conf.confException import LOGIN_ERRORS



# 错误日志的输出
class RaizeCurrentException(Exception):

    def __init__(self, err):
        # 定义错误描述
        self.desc = 'error type is "{0}"'.format(err)
        self.name = err
        self.reason = LOGIN_ERRORS[err]  # 获取Access_Token错误集
        self.location = sys._getframe().f_code.co_name   # 定义错误所在位置
        self.function = sys._getframe().f_back.f_code.co_name  # 定义错误所在函数


# 获取Access_Token错误集
class LoginException(Exception):

    # 类的初始化
    # 传入dict类，'Message'标签内标注错误类型
    def __init__(self, err):
        # 定义错误描述
        self.desc = 'error type is "{0}"'.format(err)
        self.name = err
        self.reason = LOGIN_ERRORS[err]  # 获取Access_Token错误集
        self.location = sys._getframe().f_code.co_name   # 定义错误所在位置
        self.function = sys._getframe().f_back.f_code.co_name  # 定义错误所在函数

    # def output_error




class Dada_Redis_exception(Exception):
    '''
     Custom exception types
    '''
    # 类的初始化

    def __init__(self, parameter):
        # 定义错误描述
        err = 'error type is "{0}"'.format(parameter)
        Exception.__init__(self, err)
        self.parameter = parameter  # 定义错误类型
        self.desc = "需上传Dada_Redis类型"  # 定义错误原因

# 参数类别错误集


class TypeException(Exception):
    # 类的初始化
    #待排查错误的参数统一进入list类
    def __init__(self, param):
        # 定义错误描述
            err = 'error type is "{0}".'.format(type(param))
            Exception.__init__(self, err)
            self.parameter = type(param)  # 定义错误类型
            self.desc = '并不是指定参数类别，请检查'  # 定义错误原因

# 参数数值错误集


class Dada_notcorrectparam_exception(Exception):
    '''
         Custom exception types
        '''

    # 类的初始化
    def __init__(self, parameter):
        # 定义错误描述
        err = 'error type is "{0}"'.format(parameter['Message'])
        Exception.__init__(self, err)
        self.parameter = parameter['Message']  # 定义错误类型
        self.desc = "参数值传递错误，请查看"  # 定义错误原因


# 获取空列表错误集
class Dada_emptylist_exception(Exception):
    '''
        Custom exception types
        '''

    # 类的初始化
    def __init__(self, parameter):
        # 定义错误描述
        err = 'current type is "{0}'.format(parameter)
        Exception.__init__(self, err)
        self.parameter = "空列表错误"  # 定义错误类型
        self.desc = '列表为空，无法进行之后的操作'  # 定义错误原因


# 获取搜索结果为空错误
class Dada_noexactfiled_exception(Exception):
    '''
        Custom exception types
        '''

    # 类的初始化
    def __init__(self, parameter):
        # 定义错误描述
        err = 'no fields called "{0}'.format(parameter)
        Exception.__init__(self, err)
        self.parameter = "空指针错误"  # 定义错误类型
        self.desc = '搜索不到指定名称，无法进行之后的操作'  # 定义错误原因


# 获取无权限操作错误集
class Dada_noauthority_exception(Exception):
    '''
        Custom exception types
        '''

    # 类的初始化
    def __init__(self, parameter):
        # 定义错误描述
        err = 'no authority to read or reviese "{0}'.format(parameter)
        Exception.__init__(self, err)
        self.parameter = "空指针错误"  # 定义错误类型
        self.desc = '无权限查看或者修改字段，无法进行之后的操作'  # 定义错误原因


# 获取空子表错误集合

# 获取删除失败错误集
class Dada_nodelete_exception(Exception):
    '''
        Custom exception types
        '''

    # 类的初始化
    def __init__(self, parameter):
        # 定义错误描述
        err = 'no authority to read or reviese "{0}'.format(parameter)
        Exception.__init__(self, err)
        self.parameter = "删除失败"  # 定义错误类型
        self.desc = '删除失败，请查看是否有删除权限'  # 定义错误原因

# 获取搜索结果为空错误


class Dada_norediskey_exception(Exception):
    '''
        Custom exception types
        '''

    # 类的初始化
    def __init__(self, parameter):
        # 定义错误描述
        err = 'no redis key called "{0}'.format(parameter)
        Exception.__init__(self, err)
        self.parameter = "空指针错误"  # 定义错误类型
        self.desc = '搜索不到指定名称，无法进行之后的操作'  # 定义错误原因


# 获取搜索结果为空错误
class Dada_emptykey_exception(Exception):
    '''
        Custom exception types
        '''

    # 类的初始化
    def __init__(self, parameter):
        # 定义错误描述
        err = 'no redis key called "{0}'.format(parameter)
        Exception.__init__(self, err)
        self.parameter = "空录入错误"  # 定义错误类型
        self.desc = '录入key不能为空，无法进行之后的操作'  # 定义错误原因

# 获取搜索结果为空错误


class Dada_failtoredis_exception(Exception):
    '''
        Custom exception types
        '''

    # 类的初始化
    def __init__(self, parameter):
        # 定义错误描述
        err = 'no redis key called "{0}'.format(parameter)
        Exception.__init__(self, err)
        self.parameter = "HOST OR PORT错误"  # 定义错误类型
        self.desc = '无法连接主机，无法进行之后的操作'  # 定义错误原因
