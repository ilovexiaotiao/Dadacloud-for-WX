# -*- coding: utf-8 -*-
from core.login import DadaLogin, DadaToken
from core.rediser import DadaRedis
from conf.confLogin import LOGIN_PRARM
from conf.confRedis import REDIS_PARAM
import time

# 测试计数器类
class TestClock(object):
    # 类的初始化
    def __init__(self, test_target):
        self.test_target = test_target

    # 刷新测试
    def refresh_test(self, second, times):
        for j in range(0, times):
            self.test_target.output()
            self.test_target.token.insert_token()
            for i in range(0, second):
                second_count = i + 1
                print "-----counting second-----:" + str(second_count)
                time.sleep(1)


# 激活登录状态


class TestLogin(object):
    # 类的初始化
    def __init__(self, logins, rediss, tokens):
        self.login = logins
        self.redis = rediss
        self.token = tokens
    # 输出类（后期会重写）

    def output(self):
        print "测试结果如下："
        print "--------------LOGIN类------------------------"
        print "客户名称-->" + self.login.clientId
        print "用户名称-->" + self.login.userName
        print "客户密码-->" + self.login.clientSecret
        print "用户密码-->" + self.login.passWord
        print "LOGIN生效时间-->" + self.login.initialTime
        print "LOGIN失效时间-->" + self.login.expireTime
        print "--------------TOKEN类------------------------"
        print "TOKEN生效时间-->" + self.token.initialTime
        print "TOKEN失效时间-->" + self.token.expireTime
        print "TOKEN刷新次数-->" + str(self.token.refreshCount)
        print "ACCESSTOKEN-->" + self.token.accessToken
        print "REFRESHTOKEN-->" + self.token.refreshToken
        print "--------------REDIS类------------------------"
        print"REDIS的KEY值-->" + self.token.keyName
        if self.redis.get(self.token.keyName):
            print "REDIS的VALUE值-->" + self.redis.get(self.token.keyName)
        else:
            print "没有REDIS的Value值"
        # self.token.insert_token()
        # time.sleep(3)


# 开始测试登录
if __name__ == '__main__':
    login = DadaLogin(
        username=LOGIN_PRARM['userName'],
        password=LOGIN_PRARM['passWord'],
        client=LOGIN_PRARM['clientId'],
        secret=LOGIN_PRARM['clientSecret'])
    redis = DadaRedis(
        host=REDIS_PARAM['host'],
        port=REDIS_PARAM['port'],
        login=login)
    token = DadaToken(login, redis)
    login_test = TestLogin(login, redis, token)
    # 新建测试登录的计时器
    clock = TestClock(login_test)
    # 共测试两次，间隔6秒
    clock.refresh_test(6, 4)