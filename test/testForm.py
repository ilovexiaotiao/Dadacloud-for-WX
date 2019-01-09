# -*- coding: utf-8 -*-
from core.login import DadaLogin, DadaToken
from core.rediser import DadaRedis
from conf.confLogin import LOGIN_PRARM
from conf.confRedis import REDIS_PARAM
from core.form import FormModule,DadaForm,FormEntity
import time


# 测试计数器类
class TestClock(object):
    # 类的初始化
    def __init__(self, test_target):
        self.test_target = test_target

    # 刷新测试
    def refresh_test(self):
        print self.test_target.get_module_list()[0]




# 激活登录状态
class TestLogin(object):
    # 类的初始化
    def __init__(self, logins, rediss, tokens):
        self.login = logins
        self.redis = rediss
        self.token = tokens

class TestForm(object):
    # 类的初始化
    def __init__(self, formmodule):
        self.module = formmodule



# 开始测试登录
if __name__ == '__main__':
    login = DadaLogin(
        username=LOGIN_PRARM['userName'],
        password=LOGIN_PRARM['passWord'],
        client=LOGIN_PRARM['clientId'],
        secret=LOGIN_PRARM['clientSecret'])
    redis = DadaRedis(login,
        host=REDIS_PARAM['host'],
        port=REDIS_PARAM['port'],
        )
    token = DadaToken(login, redis)
    accesstoken = token.insert_token()
    form =DadaForm(login,accesstoken)
    formmodule = FormModule(form)
    moduleid = formmodule.get_module_list()[0]['Id']
    formentity = FormEntity(form,moduleid)
    entitylist = formentity.get_entity_list()
    fieldname = formentity.get_entity_fields_name()
    print entitylist,fieldname



