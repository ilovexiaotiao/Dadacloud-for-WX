# -*- coding: utf-8 -*-
import requests
import json
from flask import Flask, render_template, request
import conf.CONFIG
import core.others.custom_exception
from get_entity import Dada_entity
from get_module import Dada_module
from core.login.login_dadayun import Dada_login
from get_fields import Dada_fields

# 搭搭云实体操作类：
# 1，此流程获取token适合开发者没有自己的web服务器，且应用为原生程序，即客户端应用（同时应用无法与浏览器交互，但是可以外调用浏览器）
# 2，需先完成模板定义验证，才可以进行表单操作。
# 3，分为两三个模块，新建、修改和删除模块，通过POST、PUT、DELETE形式，推送Access_Token和相应字段到API平台，返回JSON数据。


class Dada_entity_operate(object):
    # 类的初始化
    def __init__(self, token, moduleid):
        # 初始判断module参数是否为Dada_module类
        try:
            self.token=token
            self.moduleid = moduleid
            intype = isinstance(self.token, Dada_login)
            if not intype:
                raise (core.others.custom_exception.Dada_notcorrecttype_exception(self.token))
            # 调用表单错误类，查看错误日志
        except core.others.custom_exception.Dada_notcorrecttype_exception, a:
            print '错误概述--->', a
            print '错误类型--->', a.parameter
            print '错误原因--->', a.desc
        else:
            # 初始赋值
            self.accesstoken = token.get_token()
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                "Content-Type": "application/json; charset=utf-8",
                #采用表头传参方式，将Access_Token发送至API平台
                #'Authorization':'Bearer 4450e9d4415202a907d0408d3193b749fe021c3bd9a8a76ef8e0817cddcc7247'
                'Authorization': 'Bearer ' + self.accesstoken
                }

    #def get_instancedate(self):



    #新建实体
    def create_entity(self):
        paramsstr=     '?keyOption='+conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['keyOption']\
                    + '&containsAuthority='+conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['containsAuthority']
        headers = self.headers
        #生成JSONDATAFORM格式的表單
        instancedate={
                         "Title": "asdfasde1112",
                         "Field1": "2018-05-25T02:04:24.567Z",
                         "input": "ceshi1",
                                 }
        #生成POST Request Body
        datas={
                "IsSubmit": conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['IsSubmit'],
                "InstanceData":instancedate,
                "AutoFillMode": conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['AutoFillMode']
                }
        #合成GET形式URL
        url ='https://api.dadayun.cn/v1/form/templates/'+self.moduleid+'/instances'+paramsstr
        #对应的JSON格式，通过json-datas上传API平台
        response = requests.post(url=url, json=datas, headers=headers)
        result_create = json.loads(response.content)
        #返回新申请的表单的信息
        return result_create



        # try:
        #     response = requests.get(url=url, data=datas,headers=headers)
        #     result_entityfields = json.loads(response.content)
        #     # print(type(result_entityfields))
        #     if result_entityfields.has_key('Message'):
        #         # print "OK"
        #         raise (core.others.custom_exception.Dada_notcorrectparam_exception(result_entityfields))
        #     # 调用参数错误类，查看错误日志
        # except core.others.custom_exception.Dada_notcorrectparam_exception, x:
        #     print '错误概述--->', x
        #     print '错误类型--->', x.parameter
        #     print '错误原因--->', x.desc
        #     # 成功获取指定表单数据，返回JSON格式源
        # else:
        #     return result_entityfields

tokens=Dada_login(conf.CONFIG.USERNAME,conf.CONFIG.PASSWORD,conf.CONFIG.CLIENNT_ID,conf.CONFIG.CLIENT_SECRET)
#form= Dada_entity_operate(tokens,'c083025d-c134-4c5c-846c-740af79b360c')
form= Dada_entity_operate(tokens,'c083025d-c134-4c5c-846c-740af79b360c')
form.create_entity()



