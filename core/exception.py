# -*- coding: utf-8 -*-
import time
import sys
from conf.confException import LOGIN_ERRORS, TYPE_ERRORS, EMPTY_ERRORS





# 错误日志的输出
class RaizeCurrentException(Exception):

    def __init__(self, err, login):
        # 定义错误描述
        now = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime(
                time.time()))
        self.login = login
        self.initialTime = now
        self.userName = login.userName
        self.clientId = login.clientId
        self.err = err

    def output(self):
        print "--------------------------------------"
        print '当前用户--->', self.clientId + '/' + self.userName
        print '错误时间--->', self.initialTime
        print '错误概述--->', self.err.desc
        print '错误位置--->', self.err.location
        print '错误函数--->', self.err.function
        print '错误原因--->', self.err.reason
        print "--------------------------------------"

    def log(self):
        return True


# 搭搭云微信自定义错误类：
# 1，此流程获取token适合开发者没有自己的web服务器，且应用为原生程序，即客户端应用（同时应用无法与浏览器交互，但是可以外调用浏览器）
# 2，主要采用的是OAuth2.0请求签名机制，开发者可根据需要及应用场景使用其中一种认证即可调用搭搭云OpenAPI。
# 3，通过POST形式，推送用户名，用户密码，客户ID，客户Secret到API平台，获取Access_Token和Refresh_Token。




# 登录错误集
class LoginException(Exception):

    # 类的初始化
    # 传入dict类，'Message'标签内标注错误类型
    def __init__(self, err):
        # 定义错误描述
        self.desc = 'error type is login class ---- "{0}"'.format(err)
        self.type = err
        self.reason = LOGIN_ERRORS[err]  # 获取Access_Token错误集
        self.location = sys._getframe().f_code.co_name   # 定义错误所在位置
        self.function = sys._getframe().f_back.f_code.co_name  # 定义错误所在函数

    # def output_error


# 类别错误集
class TypeException(Exception):
    # 类的初始化
    # 待排查错误的参数统一进入list类
    def __init__(self, err):
        # 定义错误描述
        self.desc = 'error type is type class ---- "{0}"'.format(err)
        self.type = err
        self.reason = TYPE_ERRORS[err]  # 获取Type错误集
        self.location = sys._getframe().f_code.co_name   # 定义错误所在位置
        self.function = sys._getframe().f_back.f_code.co_name  # 定义错误所在函数


# 空指针错误集
class EmptyException(Exception):

    # 类的初始化
    def __init__(self, err):
        # 定义错误描述
        self.desc = 'error type is empty class ---- "{0}"'.format(err)
        self.type = err
        self.reason = EMPTY_ERRORS[err]  # 获取EMPTY错误集
        self.location = sys._getframe().f_code.co_name   # 定义错误所在位置
        self.function = sys._getframe().f_back.f_code.co_name  # 定义错误所在函数


# 权限错误集

class AuthorityException(Exception):

    # 类的初始化
    def __init__(self, err):
        # 定义错误描述
        self.desc = 'error type is authority class ---- "{0}"'.format(err)
        self.type = err
        self.reason = EMPTY_ERRORS[err]  # 获取EMPTY错误集
        self.location = sys._getframe().f_code.co_name   # 定义错误所在位置
        self.function = sys._getframe().f_back.f_code.co_name  # 定义错误所在函数


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
