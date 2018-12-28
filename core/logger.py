# -*- coding: utf-8 -*-

from exception import TypeException,RaizeCurrentException
import logging
import os,sys
from logging import handlers
from conf.confException import LOGIN_ERRORS, TYPE_ERRORS, EMPTY_ERRORS
from conf.confLogger import LOGGER_FORMAT_PARAM,LOGGER_PARAM
# from core.login import DadaLogin,DadaToken
# from core.rediser import DadaRedis



# 搭搭云微信日志：
# 1，获取用户各个操作节点的操作记录，比如Login，Form等
# 2，获取用户访问页面信息和停留时间，如Lesson_lists等
# 3，规定平台错误和警告输出格式，如LoginException等
# 4，一个Login类只保留一个Logger，之后的Token，form都使用这个Logger类


class DadaLogger(object):
    # 定义日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    # 类的初始化，默认为info集，日志备份数为1
    def __init__(self,login,level='info',when='D',backCount=1,fmt=LOGGER_FORMAT_PARAM):
        # 引入Login类信息的主要信息
        self.userName =  login.clientId+'-'+login.userName  # 搭搭云对应产品的APIKEY
        self.initialTime = login.initialTime
        self.expireTimeStrut = login.expireTimeStrut
        self.expireTime = login.expireTime
        # 以“客户编号+用户ID”作为Login类日志文件名
        filename = LOGGER_PARAM['filepath']+self.userName+'.txt'
        if not (os.path.exists(filename)):
            print os.path.exists(filename)
            file = open(filename, 'w')
            file.close()
            print('Done')
        #生成log实例
        self.logger = logging.getLogger(filename)
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

    # DadaLogin类日志
    # 请求Login类日志
    def log_login_request(self):
        userName = self.userName
        logger_statement = "DadaLogin Request is created by "+userName+".\r"
        self.logger.info(logger_statement)
        return True


    # ExpiredException中的Login类错误日志
    def log_loginexpiredexception(self,err):
        userName = self.userName
        logger_statement = "Dadalogin is expired in function('"+ err.function + "') in class('"+ err.location +"').\r"
        self.logger.error(logger_statement)
        return True

    # LoginException错误日志
    def log_loginexception(self,err):
        userName = self.userName
        logger_statement = "DadaLogin is invalid in function('"+ err.function + "') in class('"+ err.location +"')\r"
        self.logger.info(logger_statement)
        self.logger.error(err)
        return True


    # LOGIN类HTTP返回日志
    def log_http_response(self,httpcode):
        statement = "HTTP response is recieved with a status code of "+str(httpcode)+'\r'
        self.logger.info(statement)
        return True

    # LOGIN类建立成功
    def log_login_success(self):
        userName = self.userName
        logger_statement = "DadaLogin is successfully created by "+userName+" and will expired in"+ self.expireTime+"\r"
        self.logger.info(logger_statement)
        return True


    # DaDaToken类日志
    # 请求Token类日志
    def log_token_request(self):
        userName = self.userName
        logger_statement = "DadaToken Request is created by "+userName+".\r"
        self.logger.info(logger_statement)
        return True

    # TypeException错误日志
    def log_typeexception(self,err):
        userName = self.userName
        logger_statement = "ClassType is incorrect in function('"+ err.function + "') in class('"+ err.location +"')\r"
        self.logger.info(logger_statement)
        self.logger.error(err)
        return True


    def log_token_success(self):
        statement = "DadaLogin Request is successfully created by "+self.userName+" and will expired in"+ self.expireTime+"\r"
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

    def log_tokenexpiredexception(self,err):
        userName = self.userName
        logger_statement = "DadaToken created by "+userName+" is expired in function('"+ err.function + "') in class('"+ err.location +"').\r"
        self.logger.info(logger_statement)
        self.logger.error(err)
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

    def key_emptyexception(self,err):
        statement = "Redis key is empty \r"
        self.logger.info(statement)
        self.logger.error(err)
        return True

    def key_notexsitexception(self,err):
        statement = "Redis key is not exsit \r"
        self.logger.info(statement)
        self.logger.error(err)
        return True
