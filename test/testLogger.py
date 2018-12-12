# -*- coding: utf-8 -*-
from core.login import DadaLogin, DadaToken
from core.logger import DadaLogger
from core.rediser import DadaRedis
from conf.confLogin import LOGIN_PRARM
from conf.confRedis import REDIS_PARAM
import time

# 开始测试登录
if __name__ == '__main__':
    login = DadaLogin(
        username=LOGIN_PRARM['userName'],
        password=LOGIN_PRARM['passWord'],
        client=LOGIN_PRARM['clientId'],
        secret=LOGIN_PRARM['clientSecret'])
    logger = DadaLogger()
    logger.log_login(login)
