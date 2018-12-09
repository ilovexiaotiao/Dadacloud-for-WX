# -*- coding: utf-8 -*-
from core.login import DadaLogin,DadaToken
from core.others import DadaRedis
from conf.confLogin import LOGIN_PRARM
from conf.confRedis import REDIS_PARAM
import time


# 测试计数器类
class TestClock(object):
    # 类的初始化
    def __init__(self, test_target):
        self.test_target = test_target

    # 刷新测试
    def refresh_test(self, second,times):
        for j in range(0, times):
            self.test_target.output()
            for i in range(0, second):
                second_count = i+1
                print "-----counting second-----:"+str(second_count)
                time.sleep(1)

# 激活登录状态
class TestLogin(object):
    # 类的初始化
    def __init__(self):
        self.login = DadaLogin(username=LOGIN_PRARM['userName'], password=LOGIN_PRARM['passWord'],
                               client=LOGIN_PRARM['clientId'],
                                secret=LOGIN_PRARM['clientSecret'])
        self.redis = DadaRedis(host=REDIS_PARAM['host'], port=REDIS_PARAM['port'])
        self.token = DadaToken(self.login, self.redis)

    # 输出类（后期会重写）
    def output(self):
        print "测试结果如下："
        print "--------------LOGIN类------------------------"
        print "客户名称-->" + self.login.clientId
        print "用户名称-->" + self.login.userName
        print "客户密码-->" + self.login.clientSecret
        print "用户密码-->" + self.login.passWord
        print "--------------TOKEN类------------------------"
        print "TOKEN生效时间-->" + self.token.start
        print "TOKEN失效时间-->" + self.token.end
        print "EXPIRE时间-->" + str(self.token.expiretime)
        print "ACCESSTOKEN-->" + self.token.accesstoken
        print "REFRESHTOKEN-->" + self.token.refreshtoken
        print "--------------REDIS类------------------------"
        print"REDIS的KEY值-->" + self.token.key
        if self.redis.get(self.token.key):
            print "REDIS的VALUE值-->" + self.redis.get(self.token.key)
        else:
            print "没有REDIS的Value值"


# 开始测试登录
if __name__ == '__main__':
    # 新建登录测试类
    login_test = TestLogin()
    # 新建测试登录的计时器
    clock = TestClock(login_test)
    # 共测试两次，间隔6秒
    clock.refresh_test(6, 2)



