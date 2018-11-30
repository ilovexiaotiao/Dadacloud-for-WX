# -*- coding: utf-8 -*-
import requests
import json
import time
import conf.CONFIG
import sys
reload(sys)

#获取Access_Token错误集
class Dada_login_exception(Exception):
    '''
     Custom exception types
    '''
    #类的初始化
    def __init__(self, parameter):
        # 定义错误描述
        err = 'error type is "{0}"'.format(parameter)
        Exception.__init__(self, err)
        self.parameter = parameter        #定义错误类型
        self.desc = conf.CONFIG.LOGIN_ERRORS[parameter]    #定义错误原因


#参数类别错误集
class Dada_notcorrecttype_exception(Exception):
    '''
         Custom exception types
        '''

    # 类的初始化
    def __init__(self, parameter):
        # 定义错误描述
        err = 'current type is "{0}".'.format(type(parameter))
        Exception.__init__(self, err)
        self.parameter = type(parameter)  # 定义错误类型
        self.desc = '并不是指定参数类别，请检查'  # 定义错误原因

#参数数值错误集
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



#获取空列表错误集
class Dada_emptylist_exception(Exception):
    '''
        Custom exception types
        '''

    # 类的初始化
    def __init__(self,parameter):
    # 定义错误描述
        err = 'current type is "{0}'.format(parameter)
        Exception.__init__(self, err)
        self.parameter = "空列表错误"  # 定义错误类型
        self.desc = '列表为空，无法进行之后的操作'  # 定义错误原因


# 获取空列表错误集
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


# 获取空列表错误集
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




