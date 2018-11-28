# -*- coding: utf-8 -*-
import requests
import json
from flask import Flask, render_template, request
import conf.CONFIG
import core.others.custom_exception
from get_entity import Dada_entity
from get_module import Dada_module
from core.login.login_dadayun import Dada_login

# 搭搭云图表实体类：
# 1，此流程获取token适合开发者没有自己的web服务器，且应用为原生程序，即客户端应用（同时应用无法与浏览器交互，但是可以外调用浏览器）
# 2，需先完成模板定义验证，才可以进行表单操作。
# 3，分为两大模块，查询模块，通过GET形式，推送Access_Token和相应字段到API平台，返回JSON数据。
# 4，操作模块，通过POST、DELETE形式，推送Access_Token和相应JSON数据到API平台，返回提示信息。


class Dada_fields(object):
    #类的初始化
    def __init__(self,entity,entityid):
        #初始判断module参数是否为Dada_entity类
        try:
            self.entity= entity
            self.entityid=entityid
            intype=isinstance(self.entity,Dada_entity)
            if not intype:
                raise (core.others.custom_exception.Dada_notcorrecttype_exception(self.entity))
            # 调用表单错误类，查看错误日志
        except core.others.custom_exception.Dada_notcorrecttype_exception,a:
            print '错误概述--->', a
            print '错误类型--->', a.parameter
            print '错误原因--->', a.desc
        else:
            # 初始赋值
            self.moduleid=entity.moduleid
            self.headers = entity.headers


    #获取实体的字段
    def get_entity(self):
        paramsstr = '?keyOption=' + conf.CONFIG.MODULE_ENTITY_ID_PARAMS['keyOption'] \
                    + '&fields=' + conf.CONFIG.MODULE_ENTITY_ID_PARAMS['fields'] \
                    + '&containsAuthority=' + conf.CONFIG.MODULE_ENTITY_ID_PARAMS['filter']
        headers = self.headers
        url = 'https://api.dadayun.cn/v1/form/templates/' + self.moduleid + '/instances/' + entityid + paramsstr
        # 将上述参数发送至API平台，获取指定表单实体内容
        try:
            response = requests.get(url=url, headers=headers)
            result = json.loads(response.c)
            if result.has_key('error'):
                raise (core.others.custom_exception.Dada_notcorrectparam_exception(result['error']))
        # 调用参数错误类，查看错误日志
        except core.others.custom_exception.Dada_notcorrectparam_exception, x:
            print '错误概述--->', x
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc

        # 成功获取指定表单数据，返回JSON格式源
        else:
            return result


token=Dada_login(conf.CONFIG.USERNAME,conf.CONFIG.PASSWORD,conf.CONFIG.CLIENNT_ID,conf.CONFIG.CLIENT_SECRET)
module=Dada_module(token)
entity=Dada_entity(module,'2941999b-b7bb-4b59-9e23-7015d968fae9')
fields=Dada_fields(entity,'bde13ecc-87a0-4b37-bc10-d63844d8374d')
print (fields)
