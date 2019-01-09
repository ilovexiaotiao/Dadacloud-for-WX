# -*- coding: utf-8 -*-
import requests
import json
from exception import LoginException, TypeException, RaizeCurrentException,ExpiredException
from rediser import DadaRedis
from conf.confLogin import LOGIN_PRARM,LOGIN_URL,LOGIN_HEADERS,TOKEN_PARAM
from conf.confRedis import REDIS_PARAM
from conf.confConstant import ConstantTime
from core.logger import DadaLogger


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
    def __init__(self,username, password, client, secret):
        # 初始赋值
        self.userName = username  # 用户名
        self.passWord = password  # 密码（加密显示未实现）
        self.clientId = client  # 搭搭云对应产品的APIKEY
        self.clientSecret = secret  # 搭搭云对应产品的APISECRET
        # 创建时间常量，分别获取当前时间和Login失效时间
        self.conTime = ConstantTime(LOGIN_PRARM['expireSecond'])
        self.initialTime = self.conTime.now_time_string()
        self.expireTimeStrut = self.conTime.expire_time()
        self.expireTime = self.conTime.expire_time_string()
        # 定义当前用户的Logger类
        self.logger = DadaLogger(self)
        # 打印Logger日志——请求Login类
        self.logger.log_login_request()
        # 打印Logger日志——LOGIN类建立成功
        self.logger.log_login_success()



    # 首次获取Token信息，用于DadaToken首次申请AccessToken信息

    def get_connect(self):
        try:
            # 判断Login类是否过期
            if self.conTime.get_expire():
                raise (
                    ExpiredException('expire_error'))
        # 调用登录错误类
        except ExpiredException as x:
            # 打印Logger日志——LoginException类
            self.logger.log_loginexpiredexception(x)
        else:
            # 组合GET参数
            params = {
                'client_id': self.clientId,
                'client_secret': self.clientSecret,
                'grant_type': "password",
                'username': self.userName,
                'password': self.passWord,
            }
            url = LOGIN_URL
            headers = LOGIN_HEADERS
            try:
                # 通过Get方式获取Token信息
                response = requests.post(url=url, data=params, headers=headers)
                result_connect = json.loads(response.content)
                # 获取当前Response的状态码
                httpcode = response.status_code
                # 打印LoginException错误日志
                self.logger.log_http_response(httpcode)
                # 判断返回结果中是否有错误提示
                if 'error' in result_connect:
                    raise (
                        LoginException(
                            result_connect['error']))
            # 调用登录错误类，查看错误日志
            except LoginException as x:
                # 打印LoginException错误日志
                self.logger.log_loginexception(x)
            else:
                # 成功获取Access_Token和Refresh_Token,
                return result_connect

    # 后期重复获取Token，用于DadaToken重复申请AccesToken信息

    def get_refresh(self, refresh):
        try:
            if self.conTime.get_expire():
                raise (
                    ExpiredException(
                        'expire_error'))
        # 调用登录错误类，查看错误日志
        except ExpiredException as x:
            self.logger.log_loginexpiredexception()
        else:
            # 组合get参数
            params = {
                'client_id': self.clientId,
                'client_secret': self.clientSecret,
                'grant_type': "refresh_token",
                'refresh_token': refresh,
                'scope': 'openapi offline_access',
            }
            url = LOGIN_URL
            headers = LOGIN_HEADERS
            # Refresh的POST参数，与Access的有所不同
            # 通过Refresh_Token延长授权时间
            # 将上述参数发送至API平台，获取新的Access_Token和Refresh_Token
            try:
                # 发送GET请求
                response = requests.post(url=url, data=params, headers=headers)
                result_refresh = json.loads(response.content)
                # 获取当前Response的状态码
                httpcode = response.status_code
                # 打印LoginException错误日志
                self.logger.log_http_response(httpcode)
                # 判断返回结果中是否有错误提示
                if 'error' in result_refresh:
                    raise (
                        LoginException(
                            result_refresh['error']))
                # 调用登录错误类，查看错误日志
            except LoginException as x:
                self.logger.log_loginexception(x)
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
    def __init__(self,login, redis):
        # 定义当前用户的Logger类
        self.logger=login.logger
        # 打印Logger日志——请求Token类
        self.logger.log_token_request()
        self.conTime = ConstantTime(
            # TOKEN失效期
            TOKEN_PARAM['expireSecond'],
            types=1,
            # DadaLogin类失效期
            expire_time_login=login.expireTimeStrut)
        self.initialTime = self.conTime.now_time_string()
        self.expireTimeStruct = self.conTime.expire_time()
        self.expireTime = self.conTime.expire_time_string()
        # 引入DadaRedis类
        self.redisInstance = redis
        # 引入DadaLogin类
        self.loginInstance = login
        # 初始化刷新次数
        self.refreshCount = 0
        # 初始化Token
        self.accessToken = TOKEN_PARAM['accessToken']
        self.refreshToken = TOKEN_PARAM['refreshToken']
        # 将初始值存入Redis数据库
        self.keyName = REDIS_PARAM['keyName']
        try:
            # 判断login是否为DadaLogin类
            intype_login = isinstance(login, DadaLogin)
            if not intype_login:
                raise (
                    TypeException(
                        'not_login_type'))
            # 调用表单错误类，查看错误日志
        except TypeException as a:
            # 打印 TypeException错误日志
            self.logger.log_typeexception(a)
        else:
            try:
                intype_redis = isinstance(redis, DadaRedis)
                if not intype_redis:
                    raise (
                        TypeException(
                            'not_redis_type'))
                # 调用表单错误类，查看错误日志
            except TypeException as b:
                self.logger.log_typeexception(b)
                # 打印 TypeException错误日志
                self.logger.log_typeexception(a)
            else:
                    # 调用login的get_connect 方法
                    result = login.get_connect()
                    # 获取初始的Token和refreshtoken，并逐个打印
                    self.logger.log_token_success()
                    self.accessToken = result['access_token']
                    self.logger.log_get_accesstoken(self.accessToken)
                    self.refreshToken = result['refresh_token']
                    self.logger.log_get_refreshtoken(self.refreshToken)
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
        # time.sleep(3)
        try:
            if self.conTime.get_expire():
                raise (
                    ExpiredException(
                        'expire_error'))
        # 调用登录错误类，查看错误日志
        except ExpiredException as x:
            self.logger.log_tokenexpiredexception(x)
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
                self.logger.log_get_accesstoken(self.accessToken)
                self.refreshToken = result['refresh_token']
                self.logger.log_get_refreshtoken(self.refreshToken)
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
