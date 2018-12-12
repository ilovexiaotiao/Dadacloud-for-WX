# -*- coding: utf-8 -*-

from exception import TypeException,RaizeCurrentException
import logging
from logging import handlers
from conf.confException import LOGIN_ERRORS, TYPE_ERRORS, EMPTY_ERRORS
from conf.confLogger import LOGGER_FORMAT_PARAM,LOGGER_PARAM
# from core.login import DadaLogin,DadaToken
# from core.rediser import DadaRedis



# 搭搭云微信日志：
# 1，此流程获取token适合开发者没有自己的web服务器，且应用为原生程序，即客户端应用（同时应用无法与浏览器交互，但是可以外调用浏览器）
# 2，主要采用的是OAuth2.0请求签名机制，开发者可根据需要及应用场景使用其中一种认证即可调用搭搭云OpenAPI。
# 3，通过POST形式，推送用户名，用户密码，客户ID，客户Secret到API平台，获取Access_Token和Refresh_Token。


class DadaLogger(object):
    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    # 类的初始化
    def __init__(self,filename=LOGGER_PARAM['filename'],level='info',when='D',backCount=1,fmt=LOGGER_FORMAT_PARAM):
        #生成log实例
        self.logger = logging.getLogger(LOGGER_PARAM['filename'])
        #确定log格式
        format_str=logging.Formatter(fmt)
        #确定显示等级
        self.logger.setLevel(self.level_relations.get(level))
        sh=logging.StreamHandler()
        sh.setFormatter(format_str)
        # 指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                               encoding='utf-8')
        th.setFormatter(format_str)
        # 将Log结果输出到控制台
        self.logger.addHandler(sh)
        # 将log结果写入file
        self.logger.addHandler(th)

    #DadaLogin类日志输出
    def log_login(self,login):
        userName = login.clientId+'/'+login.userName
        expireTime = login.expireTime
        login_statement = "DadaLogin is created by "+userName+" and will expire in "+expireTime+'\r'
        self.logger.info(login_statement)
        return True


    def log_http_response(self,responeses):
        httpcode = str(responeses.status_code)
        statement = "HTTP Request is recieved with a status code of "+httpcode+'\r'
        self.logger.info(statement)
        return True

    def log_token(self, tokens):
        userName = tokens.loginInstance.clientId + '/' + tokens.loginInstance.userName
        expireTime = tokens.expireTime
        statement = "DadaToken is created by " + userName + " and will expire in " + expireTime+'\r'
        self.logger.info(statement)
        return True

    def log_get_accesstoken(self,tokens):
        statement = "AccessToken : "+tokens+" is acquired"+'\r'
        self.logger.info(statement)
        return True

    def log_get_refreshtoken(self,tokens):
        statement = "RefreshToken : "+tokens+" is acquired"+'\r'
        self.logger.info(statement)
        return True



    def log_insert_token(self,tokens):
        userName = tokens.loginInstance.clientId + '/' + tokens.loginInstance.userName
        accessToken = tokens.accessToken
        statement = "AccessToken : "+accessToken+" is used by " + userName+'\r'
        self.logger.info(statement)
        return True

    #DadaRedis类日志输出
    def log_redis_connect(self,host,port):
        statement = "DadaRedis is created within host : "+host+" and port ;"+port+"\r"
        self.logger.info(statement)

    def log_redis_findkey(self,keyname):
        statement = "Search keyName : "+keyname+" in redis\r"
        self.logger.info(statement)
        return True



    def log_redis_setkey(self,keyname,value):
        statement = "Write keyName : " + keyname + " and Value : "+value+" in redis\r"
        self.logger.info(statement)
        return True
