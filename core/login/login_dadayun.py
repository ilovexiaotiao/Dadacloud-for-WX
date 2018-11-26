# -*- coding: utf-8 -*-
import requests
import json
import time
import conf.CONFIG
import sys
reload(sys)
import core.others.login_exception


# 搭搭云微信注册类：
# 1，此流程获取token适合开发者没有自己的web服务器，且应用为原生程序，即客户端应用（同时应用无法与浏览器交互，但是可以外调用浏览器）
# 2，主要采用的是OAuth2.0请求签名机制，开发者可根据需要及应用场景使用其中一种认证即可调用搭搭云OpenAPI。
# 3，通过POST形式，推送用户名，用户密码，客户ID，客户Secret到API平台，获取Access_Token和Refresh_Token。
class Dada_login(object):
    # 类的初始化
    def __init__(self, username,password,clientid,clientsecret):
        # 初始赋值
        self.username = username
        self.password = password
        self.clientid=  clientid
        self.clientsecret=clientsecret
        #API平台报送表头、URL与参数
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        self.url= 'https://api.dadayun.cn/connect/token'
        self.params={
            'client_id': self.clientid,
            'client_secret': self.clientsecret,
            'grant_type': "password",
            'username': self.username,
            'password': self.password,
        }
        #将上述参数发送至API平台，获取Access_Token和Refresh_Token
        try:
            self.response = requests.post(url=self.url, data=self.params, headers=self.headers)
            self.result = json.loads(self.response.content)
            #判断返回结果中是否有错误提示
            if self.result.has_key('error'):
                raise (core.others.login_exception.Dada_login_exception(self.result['error']))
        #调用登录错误类，查看错误日志
        except core.others.login_exception.Dada_login_exception,x:
            print '错误概述--->', x
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
        #成功获取Access_Token和Refresh_Token， 并计算密匙生效时间和失效时间
        else:
            self.start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()+self.result['expires_in']))
            self.timestamp = time.mktime(time.localtime(time.time() + self.result['expires_in'])) #获取失效时间戳


    # #获取失效时间戳
    # def get_expired(self):
    #     #time.sleep(5)
    #     datetime=time.mktime(time.localtime(time.time()+self.result['expires_in']))
    #     return datetime

    #获取Access_Token
    def get_token(self):
        return  self.result['access_token']

    # 获取Refresh_Token
    def get_refresh(self):
        return self.result['refresh_token']

    #判断Access_Token是否过期
    def if_expired(self):
        now= time.mktime(time.localtime(time.time()))  #获取当前时间
       # print(self.get_refresh())
        # 若超过有效期，则返回True，说明Access_Token已经过期
        if now - self.timestamp > 0:
            return True

    #确保Access_Token状态有效，并延长授权时间
    def refresh_token(self):
        #判断Access是否过期，True：重新登录，False：延长登录时效
        if  self.if_expired():
        #重新登录
            username = self.username
            password = self.password
            clientid = self.clientid
            clientsecret = self.clientsecret
            return Dada_login(username,password,clientid,clientsecret)

        #通过Refresh_Token延长授权时间
        else:
            headers = self.headers
            url = self.__init__()
            #Refresh的POST参数，与Access的有所不同
            params = {
                'client_id': self.clientid,
                'client_secret': self.clientsecret,
                'grant_type': "refresh_token",
                'refresh_token': self.get_refresh(),
                'scope': 'openapi offline_access',
            }
            # 将上述参数发送至API平台，获取新的Access_Token和Refresh_Token
            try:
                #print self.get_refresh()
                response = requests.post(url=url, data=params, headers=headers)
                result = json.loads(response.content)
                # 判断返回结果中是否有错误提示
                if result.has_key('error'):
                    raise (core.others.login_exception.Dada_login_exception(result['error']))
            # 调用登录错误类，查看错误日志
            except core.others.login_exception.Dada_login_exception, x:
                print '错误概述--->', x
                print '错误类型--->', x.parameter
                print '错误原因--->', x.desc
            # 成功获取Access_Token和Refresh_Token， 并计算新的密匙生效时间和失效时间
            else:
                self.result= result
                self.start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                self.end = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + self.result['expires_in']))
                self.timestamp = time.mktime(time.localtime(time.time() + self.result['expires_in']))  # 获取失效时间戳








# a=Dada_login(conf.CONFIG.USERNAME,conf.CONFIG.PASSWORD,conf.CONFIG.CLIENNT_ID,conf.CONFIG.CLIENT_SECRET)
# print(a.result)

