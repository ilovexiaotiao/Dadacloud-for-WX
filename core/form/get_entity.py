# -*- coding: utf-8 -*-
import requests
import json
import conf.CONFIG
import core.others.custom_exception
from get_module import Dada_module
from core.login.login_dadayun import Dada_login

# 搭搭云图表实体类：
# 1，此流程获取token适合开发者没有自己的web服务器，且应用为原生程序，即客户端应用（同时应用无法与浏览器交互，但是可以外调用浏览器）
# 2，需先完成模板定义验证，才可以进行表单操作。
# 3，分为两大模块，查询模块，通过GET形式，推送Access_Token和相应字段到API平台，返回JSON数据。
# 4，操作模块，通过POST、DELETE形式，推送Access_Token和相应JSON数据到API平台，返回提示信息。


class Dada_entity(object):
    #类的初始化
    def __init__(self,token,moduleid):
        #初始判断module参数是否为Dada_module类
        try:
            self.token = token
            intype = isinstance(self.token, Dada_login)
            self.moduleid=moduleid
            if not intype:
                raise (core.others.custom_exception.Dada_notcorrecttype_exception(self.token))
            # 调用表单错误类，查看错误日志
        except core.others.custom_exception.Dada_notcorrecttype_exception,a:
            print '错误概述--->', a
            print '错误类型--->', a.parameter
            print '错误原因--->', a.desc
        else:
            # 初始赋值
            self.accesstoken = token.get_token()
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                # 'Content-Type': 'application/x-www-form-urlencoded',
                #采用表头传参方式，将Access_Token发送至API平台
                'Authorization': 'Bearer ' + self.accesstoken
            }

    #通过MODULE_ID，获取指定单据模板
    def get_entity_fields(self):
        paramsstr = '?version=' + conf.CONFIG.MODULE_ID_PARAMS['version']
        headers = self.headers
        # 合成GET形式URL
        url = 'https://api.dadayun.cn/v1/form/templates/'+self.moduleid+paramsstr
        #print url
        # 将上述参数发送至API平台，获取指定表单模板
        try:
            response = requests.get(url=url, headers=headers)
            result_entityfields = json.loads(response.content)
            #print(type(result_entityfields))
            if  result_entityfields.has_key('Message'):
                #print "OK"
                raise (core.others.custom_exception.Dada_notcorrectparam_exception(result_entityfields))
        # 调用参数错误类，查看错误日志
        except core.others.custom_exception.Dada_notcorrectparam_exception, x:
            print '错误概述--->', x
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
        # 成功获取指定表单数据，返回JSON格式源
        else:
            return result_entityfields



    # 获取指定MODULE_ID的所有表单实体列表
    def get_entity_list(self):
        paramsstr = '?limit=' + conf.CONFIG.MODULE_ENTITY_PARAMS['limit'] \
                    + '&fields=' + conf.CONFIG.MODULE_ENTITY_PARAMS['fields'] \
                    + '&filter=' + conf.CONFIG.MODULE_ENTITY_PARAMS['filter'] \
                    + '&start=' + conf.CONFIG.MODULE_ENTITY_PARAMS['start'] \
                    + '&sort=' + conf.CONFIG.MODULE_ENTITY_PARAMS['sort'] \
                    + '&count=' + conf.CONFIG.MODULE_ENTITY_PARAMS['count'] \
                    + '&keyOption' + conf.CONFIG.MODULE_ENTITY_PARAMS['keyOption']
        headers = self.headers
        # 合成GET形式URL
        url = 'https://api.dadayun.cn/v1/form/templates/' + self.moduleid + '/instances' + paramsstr
        # 将上述参数发送至API平台，获取指定表单实体列表
        try:
            response = requests.get(url=url, headers=headers)
            result_entitylist = json.loads(response.content)
            #print type(result)
            if type(result_entitylist) is dict:
                raise (core.others.custom_exception.Dada_notcorrectparam_exception(result_entitylist))
        # 调用参数错误类，查看错误日志
        except core.others.custom_exception.Dada_notcorrectparam_exception, x:
            print '错误概述--->', x
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc

        # 成功获取指定表单数据，返回JSON格式源
        else:
            return result_entitylist

    #获取已经提交的实体列表
    def get_entity_list_submit(self):
         # 先获取所有实体列表
         submit = self.get_entity_list()
         result_submit = []
         #print(type(hasinstance))
         try:
             # 判断列表是否为空，若为空，抛出异常
             if submit is None:
                 raise (core.others.custom_exception.Dada_emptylist_exception(submit))
         except core.others.custom_exception.Dada_emptylist_exception, x:
             print '错误类型--->', x.parameter
             print '错误原因--->', x.desc
         # 循环判断表单模板的“IsValid”字段是否为True,若为真，则有表单已提交
         else:
             # 成功获取表单列表数据，返回JSON格式源
             inlen = len(submit)
             for i in range(0, inlen - 1):
                 if submit[i]['IsValid'] is True:
                     result_submit.append(submit[i])
             return result_submit


    #获得未提交的实体列表
    def get_entity_list_revise(self):
        # 先获取所有实体列表
        revise = self.get_entity_list()
        result_revise = []
        # print(type(hasinstance))
        try:
            # 判断列表是否为空，若为空，抛出异常
            if revise is None:
                raise (core.others.custom_exception.Dada_emptylist_exception(revise))
        except core.others.custom_exception.Dada_emptylist_exception, x:
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
            # 循环判断表单模板的“IsValid”字段是否为True,若为真，则有表单在修改中
        else:
            # 成功获取表单列表数据，返回JSON格式源
            inlen = len(revise)
            for i in range(0, inlen - 1):
                if revise[i]['IsValid'] is False:
                    result_revise.append(revise[i])
            return result_revise


#
# token=Dada_login(conf.CONFIG.USERNAME,conf.CONFIG.PASSWORD,conf.CONFIG.CLIENNT_ID,conf.CONFIG.CLIENT_SECRET)
# module=Dada_module(token)
# entity=Dada_entity(token,'c083025d-c134-4c5c-846c-740af79b360c')
# ss=entity.get_entity_fields()
# for key,value in ss.items():
#
#     print key
#
