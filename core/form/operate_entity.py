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
# 3，分为两三个模块，新建、修改和删除模块，通过POST、DELETE形式，推送Access_Token和相应字段到API平台，返回JSON数据。


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
                'Authorization': 'Bearer ' + self.accesstoken
                }

    #新建实体
    def create_entity(self):
        paramsstr=     '?keyOption='+conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['keyOption']\
                    + '&containsAuthority='+conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['containsAuthority']
        headers=self.headers
        InstanceData={
            "Title":"asdfisdfasdf",
            'input':"asdfasdfsss111",
            'Field1':"2018-05-25T02:04:24.567Z",
                         # # 'Id':'',
                         # # "ModifyByName": "系统管理员",
                         # # 'ModifyTime': {'R': True, 'U': True, 'Value': '2018-11-30T08:53:25.437Z'},
                         # # "IsBlock": 'False',
                         # # 'ModifyBy':{'R': True, 'U': True, 'Value': 'a1e38673-ae69-4536-acac-a27dc46da856'},
                         # 'Title': {"Value": "在sdfasdf职_系统管理员",
                         #           "R": 'True',
                         #           "U": 'True'},
                         # # "IsValid": 'True',
                         # # "CreatorName": "系统管理员",
                         # 'Field1': {"Value": "2018-05-25T02:04:24.567Z",
                         #            "R": 'True',
                         #            "U": 'True'},
                         # # 'CreateTime':{'R': True, 'U': True, 'Value': '2018-11-30T08:53:25.437Z'},
                         # # 'Creator':{'R': True, 'U': True, 'Value': 'a1e38673-ae69-4536-acac-a27dc46da856'},
                         # # 'RoleAction':{ 'D': True, 'R': True, 'U': True, 'Export': False},
                         # # "DataEnable": 'True',
                         # 'input': {"Value": "ceshi",
                         #           "R": 'true',
                         #           "U": 'true'},
                         # # 'CreatorPositionId':{'R': True, 'U': True, 'Value': 'abb7fb51-fada-4608-bbea-4b35db75f2c7'},
                         # # "CreatorPosition": "系统管理员",



        }
        datas={'IsSubmit':conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['IsSubmit'],
               'InstanceData':InstanceData,
               'AutoFillMode':conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['AutoFillMode'],
               }

        #合成GET形式URL
        url ='https://api.dadayun.cn/v1/form/templates/'+self.moduleid+'/instances'+paramsstr
        response = requests.post(url=url, data=datas, headers=headers)
        result=json.loads(response.content)
        print response.status_code

        #     result_entityfields = json.loads(response.content)
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



