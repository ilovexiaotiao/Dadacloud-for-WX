# -*- coding: utf-8 -*-
from core.login.login_dadayun import Dada_login,Dada_token
from core.others.save_redis import Dada_redis
import conf.CONFIG_REDIS
import conf.CONFIG
import time

def output_login(login,redis,token):

    print "测试结果如下："
    print "--------------LOGIN类------------------------"
    print "客户名称-->" + login.clientid
    print "用户名称-->" + login.username
    print "客户密码-->" + login.clientsecret
    print "用户密码-->" + login.password
    print "--------------TOKEN类------------------------"
    print "TOKEN生效时间-->" + token.start
    print "TOKEN失效时间-->" + token.end
    print "EXPIRE时间-->" + str(token.expiretime)
    print "ACCESSTOKEN-->" + token.accesstoken
    print "REFRESHTOKEN-->" + token.refreshtoken
    print "--------------REDIS类------------------------"
    print"REDIS的KEY值-->" + token.key
    if redis.get(token.key):
        print"REDIS的VALUE值-->" + redis.get(token.key)
    else:
        print "没有REDIS的Value值"


def count_time(second):
    for i in range(0,second):
        second_count=i+1
        print "-----counting second-----:"+str(second_count)
        time.sleep(second)





login = Dada_login(conf.CONFIG.USERNAME,conf.CONFIG.PASSWORD,conf.CONFIG.CLIENNT_ID,conf.CONFIG.CLIENT_SECRET)
redis=Dada_redis(host=conf.CONFIG_REDIS.REDIS_HOST,port=conf.CONFIG_REDIS.REDIS_PORT)
token = Dada_token(login,redis)
output_login(login,redis,token)
count_time(6)
output_login(login,redis,token)
count_time(6)
output_login(login,redis,token)




