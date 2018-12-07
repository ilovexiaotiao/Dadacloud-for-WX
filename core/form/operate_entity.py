# -*- coding: utf-8 -*-
import requests
import json
from flask import Flask, render_template, request
import conf.CONFIG
import core.others.custom_exception
from get_entity import Dada_entity
from get_module import Dada_module
from core.login.login_dadayun import Dada_token,Dada_login
from get_fields import Dada_fields

# 搭搭云实体操作类：
# 1，此流程获取token适合开发者没有自己的web服务器，且应用为原生程序，即客户端应用（同时应用无法与浏览器交互，但是可以外调用浏览器）
# 2，需先完成模板定义验证，才可以进行表单操作。
# 3，分为两三个模块，新建、修改和删除模块，通过POST、PUT、DELETE形式，推送Access_Token和相应字段到API平台，返回JSON数据。


class Dada_operate(object):
    # 类的初始化
    def __init__(self, token, moduleid):
        # 初始判断module参数是否为Dada_module类
        try:
            self.token=token
            self.moduleid = moduleid
            intype = isinstance(self.token, Dada_token)
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
                #'Authorization':'Bearer e088a54d2f426caec69016163b3080a57879410d5cd53848ebec480beea79609'
                'Authorization': 'Bearer ' + self.accesstoken
                }
    #获取网页提交的表单
    def get_instancedate(self,ajaxdata):

        instancedate=ajaxdata
        return  instancedate



    #新建实体
    def create_entity(self):
        paramsstr=     '?keyOption='+conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['keyOption']\
                    + '&containsAuthority='+conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['containsAuthority']
        headers = self.headers
        instancedate = {
            "Title": 'title',
            "Field1": 'field1',
            "input": 'input',
        }
        #生成JSONDATAFORM格式的表單
        #getinstancedata=self.get_instancedate(instancedate)
        #生成POST Request Body
        datas={
                "IsSubmit": conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['IsSubmit'],
                "InstanceData":instancedate,
                "AutoFillMode": conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['AutoFillMode']
                }
        #合成GET形式URL
        url ='https://api.dadayun.cn/v1/form/templates/'+self.moduleid+'/instances'+paramsstr
        #对应的JSON格式，通过json-datas上传API平台
        try:
            response = requests.post(url=url, json=datas, headers=headers)
            result_create = json.loads(response.content)
            # print response.status_code
            if response.status_code>399:
                raise core.others.custom_exception.Dada_notcorrectparam_exception(result_create)
        except core.others.custom_exception.Dada_notcorrectparam_exception,x:
            print '错误概述--->', x
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
        #返回新申请的表单的信息
        else:
            return result_create

    #为实体的子表增加信息
    def revise_entity(self,instanceid):
        paramsstr=     '?keyOption='+conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['keyOption']\
                    + '&containsAuthority='+conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['containsAuthority']
        headers = self.headers
        #生成JSONDATAFORM格式的表單
        instancedate={

                         "Title": "asdfasdde1112",
                         "Field1": "2018-05-25T02:04:24.567Z",
                         "input": "ceshi1",
                         "table":[
                                {   "Action":"create",
                                    "start":"111",
                                  "end":"222"
                                 }
                                ]
                    }
        #生成POST Request Body
        datas={
                "IsSubmit": conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['IsSubmit'],
                "InstanceData":instancedate,
                "AutoFillMode": conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['AutoFillMode']
                }
        #合成GET形式URL
        url ='https://api.dadayun.cn/v1/form/templates/'+self.moduleid+'/instances/'+instanceid+paramsstr
        #对应的JSON格式，通过json-datas上传API平台
        try:
            response = requests.put(url=url, json=datas, headers=headers)
            result_add = json.loads(response.content)
            print response.status_code
            if response.status_code>399:
                raise core.others.custom_exception.Dada_notcorrectparam_exception(result_add)
        except core.others.custom_exception.Dada_notcorrectparam_exception,x:
            print '错误概述--->', x
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
        #返回新申请的表单的信息
        else:
            return result_add
        #返回新申请的表单的信息


    #修改实体信息
    def revise_entity_sub(self,instanceid):
        paramsstr=     '?keyOption='+conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['keyOption']\
                    + '&containsAuthority='+conf.CONFIG.MODULE_ENTITY_SEND_PARAMS['containsAuthority']
        headers = self.headers
        #生成JSONDATAFORM格式的表單
        instancedate={
                         "Action":"update",
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
        url ='https://api.dadayun.cn/v1/form/templates/'+self.moduleid+'/instances/'+instanceid+paramsstr
        #对应的JSON格式，通过json-datas上传API平台
        response = requests.post(url=url, json=datas, headers=headers)
        result_create = json.loads(response.content)
        #返回新申请的表单的信息
        return result_create

    #删除实体
    def delete_entity(self,instanceid):
        result_delete={}
        headers=self.headers
        #合成GET形式URL
        url ='https://api.dadayun.cn/v1/form/templates/'+self.moduleid+'/instances/'+instanceid
        #对应的JSON格式，通过json-datas上传API平台
        try:
            response = requests.delete(url=url,headers=headers)
            if response.status_code!=204:
                result_delete = json.loads(response.content)
                raise core.others.custom_exception.Dada_nodelete_exception(result_delete)
        except core.others.custom_exception.Dada_nodelete_exception,x:
            print '错误概述--->', x
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
        else:
            result_delete="DELETE OK"
        #返回新申请的表单的信息
            return result_delete











