# -*- coding: utf-8 -*-
from core.login.login_dadayun import Dada_login,Dada_token
from core.others.save_redis import Dada_redis
import conf.CONFIG_REDIS
import conf.CONFIG
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
        self.login = Dada_login(conf.CONFIG.USERNAME, conf.CONFIG.PASSWORD, conf.CONFIG.CLIENNT_ID,
                                conf.CONFIG.CLIENT_SECRET)
        self.redis = Dada_redis(host=conf.CONFIG_REDIS.REDIS_HOST, port=conf.CONFIG_REDIS.REDIS_PORT)
        self.token = Dada_token(self.login, self.redis)

    # 输出类（后期会重写）
    def output(self):
        print "测试结果如下："
        print "--------------LOGIN类------------------------"
        print "客户名称-->" + self.login.clientid
        print "用户名称-->" + self.login.username
        print "客户密码-->" + self.login.clientsecret
        print "用户密码-->" + self.login.password
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



