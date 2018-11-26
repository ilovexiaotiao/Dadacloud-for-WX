# -*- coding: utf-8 -*-
import requests
import json
import time
import conf.CONFIG
import sys
reload(sys)


# 定义Dada_login的API错误:
# invalid_request	请求不合法。	400	请求不合法。
# invalid_client	client_id或client_secret参数无效。	400	client_id或client_secret参数无效。
# invalid_grant	提供的凭证验证失败。	400	提供的凭证验证失败（用户名或密码为空，用户名或密码超过最大长度）。
# unauthorized_client	客户端没有权限。	400	客户端没有权限（客户端不允许此模式验证）。
# unsupported_grant_type	不支持的 GrantType。	400	不支持的 GrantType。
# invalid_scope	Scope验证失败。	400	Scope验证失败。
# temporarily_unavailable	服务暂时无法访问。	500	服务暂时无法访问。
# server_error	服务器内部错误，请联系管理员。	500	服务器内部错误，请联系管理员。


# 错误描述集合
LOGIN_ERRORS = {
    'invalid_request': '请求不合法',
    'invalid_client': 'client_id或client_secret参数无效',
    'invalid_grant': '提供的凭证验证失败',
    'unauthorized_client': '客户端没有权限',
    'unsupported_grant_type': '不支持的 GrantType',
    'invalid_scope': 'Scope验证失败',
    'temporarily_unavailable': '服务暂时无法访问',
    'server_error': '服务器内部错误，请联系管理员'
}


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
        self.desc = LOGIN_ERRORS[parameter]    #定义错误原因



