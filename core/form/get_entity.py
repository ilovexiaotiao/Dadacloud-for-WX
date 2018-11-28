# -*- coding: utf-8 -*-
import requests
import json
from flask import Flask, render_template, request
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
    def __init__(self,module,moduleid):
        #初始判断module参数是否为Dada_module类
        try:
            self.module= module
            self.moduleid=moduleid
            intype=isinstance(self.module,Dada_module)
            if not intype:
                raise (core.others.custom_exception.Dada_notcorrecttype_exception(self.module))
            # 调用表单错误类，查看错误日志
        except core.others.custom_exception.Dada_notcorrecttype_exception,a:
            print '错误概述--->', a
            print '错误类型--->', a.parameter
            print '错误原因--->', a.desc
        else:
            # 初始赋值
            self.headers = module.headers

    #通过MODULE_ID，获取指定单据模板
    def get_entity_fields(self):
        paramsstr = '?version=' + conf.CONFIG.MODULE_ID_PARAMS['version']
        headers = self.headers
        # 合成GET形式URL
        url = 'https://api.dadayun.cn/v1/form/templates/'+self.moduleid+paramsstr
        print url
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

    # def get_entity_list_submit(self):



# token=Dada_login(conf.CONFIG.USERNAME,conf.CONFIG.PASSWORD,conf.CONFIG.CLIENNT_ID,conf.CONFIG.CLIENT_SECRET)
# module=Dada_module(token)
# entity=Dada_entity(module,'2941999b-b7bb-4b59-9e23-7015d968fae9')
# print(entity.get_entity_list())

