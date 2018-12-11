# -*- coding: utf-8 -*-
import requests
import json
import time
from exception import LoginException, TypeException, RaizeCurrentException
from others import DadaRedis
from conf.confLogin import LOGIN_PRARM
from conf.confRedis import REDIS_PARAM
from conf.confConstant import ConstantTime


# 搭搭云微信注册：
# 1，此流程获取token适合开发者没有自己的web服务器，且应用为原生程序，即客户端应用（同时应用无法与浏览器交互，但是可以外调用浏览器）
# 2，主要采用的是OAuth2.0请求签名机制，开发者可根据需要及应用场景使用其中一种认证即可调用搭搭云OpenAPI。
# 3，通过POST形式，推送用户名，用户密码，客户ID，客户Secret到API平台，获取Access_Token和Refresh_Token。


# 搭搭云Login类，包含基本用户信息、关联起止时间。
# 创建搭搭注册类，意味服务器与username用户创建关联,关联时间不可延长（已实现）
# 初始创建需要输入用户名、密码等信息，Token有效期内，免密关联。（已实现）
# 若用户未续约Token，则关联类自动取消（已实现）
# 若用户登录Cookie被清除，则关联类自动取消（未实现）
# 若用户修改用户名，则关联类自动取消（未实现）
# 若用户未登录时间超过180天，则关联自动取消（已实现）
# 所有行为都需引入LOGIN类(重要）


class DadaLogin(object):
    # 类的初始化
    def __init__(self, username, password, client, secret):
        # 初始赋值
        self.userName = username  # 用户名
        self.passWord = password  # 密码（加密显示未实现）
        self.clientId = client  # 搭搭云对应产品的APIKEY
        self.clientSecret = secret  # 搭搭云对应产品的APISECRET
        # 创建时间常量
        self.conTime = ConstantTime(LOGIN_PRARM['expireSecond'])
        self.initialTime = self.conTime.now_time_string()
        self.expireTimeStrut = self.conTime.expire_time()
        self.expireTime = self.conTime.expire_time_string()

    # 首次获取Token信息

    def get_connect(self):
        try:
            print self.conTime
            print self.expireTime
            print self.conTime.get_expire()
            if self.conTime.get_expire():
                raise (
                    LoginException('expire_error'))
        # 调用登录错误类，查看错误日志
        except LoginException as x:
            output2 = RaizeCurrentException(x, self)
            output2.output()
        else:
            # 组合GET参数
            params = {
                'client_id': self.clientId,
                'client_secret': self.clientSecret,
                'grant_type': "password",
                'username': self.userName,
                'password': self.passWord,
            }
            url = 'https://api.dadayun.cn/connect/token'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/58.0.3029.110 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            try:
                # 通过Get方式获取Token信息
                response = requests.post(url=url, data=params, headers=headers)
                result_connect = json.loads(response.content)
                # 判断返回结果中是否有错误提示
                if 'error' in result_connect:
                    raise (
                        LoginException(
                            result_connect['error']))
            # 调用登录错误类，查看错误日志
            except LoginException as x:
                # 输出错误日志
                output1 = RaizeCurrentException(x, self)
                output1.output()
            # 成功获取Access_Token和Refresh_Token
            else:
                return result_connect

    # 后期重复获取Token

    def get_refresh(self, refresh):
        try:
            if self.conTime.get_expire():
                raise (
                    LoginException(
                        'expire_error'))
        # 调用登录错误类，查看错误日志
        except LoginException as x:
            output = RaizeCurrentException(x, self)
            output.output()
        else:
            # 组合get参数
            params = {
                'client_id': self.clientId,
                'client_secret': self.clientSecret,
                'grant_type': "refresh_token",
                'refresh_token': refresh,
                'scope': 'openapi offline_access',
            }
            url = 'https://api.dadayun.cn/connect/token'
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/58.0.3029.110 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            # Refresh的POST参数，与Access的有所不同
            # 通过Refresh_Token延长授权时间
            # 将上述参数发送至API平台，获取新的Access_Token和Refresh_Token
            try:
                # 发送GET请求
                response = requests.post(url=url, data=params, headers=headers)
                result_refresh = json.loads(response.content)
                # 判断返回结果中是否有错误提示
                if 'error' in result_refresh:
                    raise (
                        LoginException(
                            result_refresh['error']))
                # 调用登录错误类，查看错误日志
            except LoginException as x:
                output = RaizeCurrentException(x, self)
                output.output()
            # 成功更新Access_Token和Refresh_Token
            else:
                return result_refresh

# 搭搭云Token类，包含Token信息、获取时间。初始创建需要输入Login类和Redis类，Token在Redis里的字段是client/username
# 创建搭搭Token类，将自动获取初始ACCESSTOKEN和REFRESHTOKEN，并存入Redis数据库内（已实现）
# 若用户登录Cookie被清除，则login类和Redis自动清除（未实现）
# 若用户insert_token日期大于Token失效日期，Token自动失效（已实现）
# Token有效期不超过Login类的有效期（已实现）


class DadaToken(object):
    # 类的初始化
    def __init__(self, login, redis):
        self.conTime = ConstantTime(
            LOGIN_PRARM['expireSecond'],
            types=1,
            expire_time_login=login.expireTimeStrut)
        self.initialTime = self.conTime.now_time_string()
        self.expireTimeStruct = self.conTime.expire_time()
        self.expireTime = self.conTime.expire_time_string()
        self.redisInstance = redis
        self.loginInstance = login
        # 刷新次数
        self.refreshCount = 0
        self.accessToken = ""
        self.refreshToken = ""
        # 将初始值存入Redis数据库
        self.keyName = ""
        try:
            intype_login = isinstance(login, DadaLogin)
            if not intype_login:
                raise (
                    TypeException(
                        'not_login_type'))
            # 调用表单错误类，查看错误日志
        except TypeException as a:
            output = RaizeCurrentException(a, self)
            output.output()
        else:
            try:
                intype_redis = isinstance(redis, DadaRedis)
                if not intype_redis:
                    raise (
                        TypeException(
                            'not_redis_type'))
                # 调用表单错误类，查看错误日志
            except TypeException as b:
                output1 = RaizeCurrentException(b, self)
                output1.output()
            else:
                try:
                    # 判断返回结果中是否有错误提示
                    result = login.get_connect()
                    if self.conTime.get_expire():
                        raise (
                            LoginException(
                                'expire_error'))
                # 调用登录错误类，查看错误日志
                except LoginException as x:
                    output2 = RaizeCurrentException(x, login)
                    output2.output()
                # 在redis里面查找key值，如有，直接输出
                else:
                    # 获取初始的Token和refreshtoken
                    self.accessToken = result['access_token']
                    self.refreshToken = result['refresh_token']
                    # 将初始值存入Redis数据库
                    self.keyName = login.clientId + "/" + login.userName
                    redis.set(
                        self.keyName,
                        self.accessToken,
                        REDIS_PARAM['expiresecond'])

    # 获取Access_Token
    # 若Token在redis有效期内，在Redis查找ACCESSTOKEN
    # 若Token在redis有效期外，通过REFRESHTOKEN刷新Token，实现无密码登录

    def insert_token(self):
        time.sleep(3)
        try:
            if self.conTime.get_expire():
                raise (
                    LoginException(
                        'expire_error'))
        # 调用登录错误类，查看错误日志
        except LoginException as x:
            output2 = RaizeCurrentException(x, self.loginInstance)
            output2.output()
        # 在redis里面查找key值，如有，直接输出
        else:
            token = self.redisInstance.get(self.keyName)
            if token:
                return token
            else:
                # 如没有，通过refreshtoken重新命令获取token
                result = self.loginInstance.get_refresh(self.refreshToken)
                # 获取更新的Token和refreshtoken,替代初始Token信息
                self.accessToken = result['access_token']
                self.refreshToken = result['refresh_token']
                # 计算token时间
                self.refreshCount = self.refreshCount + 1
                contime = self.conTime = ConstantTime(
                    LOGIN_PRARM['expireSecond'],
                    types=1,
                    expire_time_login=self.loginInstance.expireTimeStrut)
                self.conTime = contime
                self.expireTimeStruct = contime.expire_time()
                self.expireTime = contime.expire_time_string()
                # 将更新Token值存入Redis数据库
                self.redisInstance.set(
                    self.keyName,
                    self.accessToken,
                    REDIS_PARAM['expiresecond'])
                return result['access_token']
