# -*- coding: utf-8 -*-
import requests
import json
import time
import core.others.custom_exception
import core.others.save_redis


# 搭搭云微信注册类：
# 1，此流程获取token适合开发者没有自己的web服务器，且应用为原生程序，即客户端应用（同时应用无法与浏览器交互，但是可以外调用浏览器）
# 2，主要采用的是OAuth2.0请求签名机制，开发者可根据需要及应用场景使用其中一种认证即可调用搭搭云OpenAPI。
# 3，通过POST形式，推送用户名，用户密码，客户ID，客户Secret到API平台，获取Access_Token和Refresh_Token。


class Dada_login(object):
    # 类的初始化
    def __init__(self, username,password, clientid, clientsecret):
        # 初始赋值
        self.username = username
        self.password = password
        self.clientid = clientid
        self.clientsecret =clientsecret
        #API平台报送表头、URL与参数



    #获取Redis中的token值
    def get_connect(self):
        params={
            'client_id': self.clientid,
            'client_secret': self.clientsecret,
            'grant_type': "password",
            'username': self.username,
            'password': self.password,
        }
        url = 'https://api.dadayun.cn/connect/token'
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        try:
            response = requests.post(url=url, data=params, headers=headers)
            result_connect = json.loads(response.content)
            # 判断返回结果中是否有错误提示
            if result_connect.has_key('error'):
                raise (core.others.custom_exception.Dada_login_exception(result['error']))
        # 调用登录错误类，查看错误日志
        except core.others.custom_exception.Dada_login_exception, x:
            print '错误概述--->', x
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
        # 成功获取Access_Token和Refresh_Token
        else:
            return result_connect

    def get_refresh(self,refresh):
        params = {
            'client_id': self.clientid,
            'client_secret': self.clientsecret,
            'grant_type': "refresh_token",
            'refresh_token': refresh,
            'scope': 'openapi offline_access',
        }
        url = 'https://api.dadayun.cn/connect/token'
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        #Refresh的POST参数，与Access的有所不同
        # 通过Refresh_Token延长授权时间
        # 将上述参数发送至API平台，获取新的Access_Token和Refresh_Token
        try:
            #print self.get_refresh()
            response = requests.post(url=url, data=params, headers=headers)
            result_refresh = json.loads(response.content)
            # 判断返回结果中是否有错误提示
            if result_refresh.has_key('error'):
                raise (core.others.custom_exception.Dada_login_exception(result_refresh['error']))
        # 调用登录错误类，查看错误日志
        except core.others.custom_exception.Dada_login_exception, x:
            print '错误概述--->', x
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
        # 成功获取Access_Token和Refresh_Token
        else:
            return result_refresh


class Dada_token(object):
    # 类的初始化
    def __init__(self, login,redis):
        # 在redis里面查找key值，如有，直接输出
        try:
            intype_login = isinstance(login, Dada_login)
            intype_redis=  isinstance(redis, core.others.save_redis.Dada_redis)
            if not (intype_redis and intype_login):
                raise (core.others.custom_exception.Dada_notcorrecttype_exception(type(redis)))
            # 调用表单错误类，查看错误日志
        except core.others.custom_exception.Dada_notcorrecttype_exception, a:
            print '错误概述--->', a
            print '错误类型--->', a.parameter
            print '错误原因--->', a.desc
        else:
            self.redis=redis
            self.login=login
            # 获取初始的Token和refreshtoken
            self.accesstoken=login.get_connect()['access_token']
            self.refreshtoken =login.get_connect()['refresh_token']
            #计算token时间
            self.expiretime= login.get_connect()['expires_in']
            # self.expiretime = 4
            self.start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + self.expiretime))
            # 将初始值存入Redis数据库
            self.key=login.clientid+"/"+login.username
            redis.set(self.key, self.accesstoken, self.expiretime)
            #刷新赋值


    #获取Access_Token
    def get_token(self):
        #在redis里面查找key值，如有，直接输出
        token =self.redis.get(self.key)
        if token:
            return token
        else:
            # 如没有，通过refreshtoken重新命令获取token
            result = self.login.get_refresh(self.refreshtoken)
            token=result['access_token']
            # 获取更新的Token和refreshtoken
            self.accesstoken=token
            self.refreshtoken =result['refresh_token']
            #计算token时间
            self.expiretime= result['expires_in']
            # self.expiretime = 4
            self.start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + self.expiretime))
            # 将初始值存入Redis数据库
            self.redis.set(self.key, self.accesstoken, self.expiretime)
            return token







