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
# 2，需先完成实体定义验证，才可以进行表单操作。
# 3，可以根据用户权限，获取具体字段。
# 4，通过GET形式，推送Access_Token和相应字段到API平台，返回JSON数据。


class Dada_fields(object):
    #类的初始化
    def __init__(self,token,moduleid,entityid):
        #初始判断module参数是否为Dada_entity类
        try:
            self.entityid=entityid
            self.moduleid = moduleid
            self.token = token
            intype = isinstance(self.token, Dada_login)
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



    #获取实体的所有字段
    def get_fields_all(self):
        paramsstr = '?keyOption=' + conf.CONFIG.MODULE_ENTITY_ID_PARAMS['keyOption'] \
                    + '&fields=' + conf.CONFIG.MODULE_ENTITY_ID_PARAMS['fields'] \
                    + '&containsAuthority=' + conf.CONFIG.MODULE_ENTITY_ID_PARAMS['containsAuthority']
        headers = self.headers
        url = 'https://api.dadayun.cn/v1/form/templates/' + self.moduleid + '/instances/' + self.entityid + paramsstr
        # 将上述参数发送至API平台，获取指定表单实体内容
        try:
            response = requests.get(url=url, headers=headers)
            result_allfields = json.loads(response.content)
            if result_allfields.has_key('error'):
                raise (core.others.custom_exception.Dada_notcorrectparam_exception(result_allfields['error']))
        # 调用参数错误类，查看错误日志
        except core.others.custom_exception.Dada_notcorrectparam_exception, x:
            print '错误概述--->', x
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
        # 成功获取指定表单数据，返回JSON格式源
        else:
            return result_allfields

    #获取实体的可读字段
    def get_fields_read(self):
        all_fields = self.get_fields_all()
        result_canread={}
        key_list=[]
        try:
            # 判断列表是否为空，若为空，抛出异常
            if all_fields is None:
                raise (core.others.custom_exception.Dada_emptylist_exception(all_fields))
        except core.others.custom_exception.Dada_emptylist_exception, x:
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
            # 循环判断表单模板的“IsValid”字段是否为True,若为真，则有表单在修改中
        else:
            # 成功获取实体字段数据，分两种情况遍历：1，返回正常值，2，返回字典值
            for key,value in all_fields.items():
                if type(value) is not dict:
                    #第一种情况，返回正常值，计入可读列表
                    key_list.append(key)
                else:
                    #第二种情况，返回字典值，计入刻度列表
                    if all_fields[key]['R'] is True:
                        key_list.append(key)
            #生成新的字典，装在可读字段列表
            result_canread=result_canread.fromkeys(key_list)
            #循环赋值
            for key,value in result_canread.items():
                result_canread[key]=all_fields[key]
            return result_canread

    # 获取实体的可修改字段
    def get_fields_revise(self):
        all_fields = self.get_fields_all()
        result_canrevise = {}
        key_list = []
        try:
            # 判断列表是否为空，若为空，抛出异常
            if all_fields is None:
                raise (core.others.custom_exception.Dada_emptylist_exception(all_fields))
        except core.others.custom_exception.Dada_emptylist_exception, x:
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
            # 循环判断表单模板的“IsValid”字段是否为True,若为真，则有表单在修改中
        else:
            # 成功获取实体字段数据，分两种情况遍历：1，返回正常值，2，返回字典值
            for key, value in all_fields.items():
                if type(value) is not dict:
                    # 第一种情况，返回正常值，计入可读列表
                    key_list.append(key)
                else:
                    # 第二种情况，返回字典值，计入刻度列表
                    if all_fields[key]['U'] is True:
                        key_list.append(key)
            # 生成新的字典，装在可修改字段列表
            result_canrevise = result_canrevise.fromkeys(key_list)
            # 循环赋值
            for key, value in result_canrevise.items():
                result_canrevise[key] = all_fields[key]
        return result_canrevise


    #获取实体的指定可读字段
    def get_fields_readexact(self,fieldname):
        all_fields = self.get_fields_read()
        hasfield=all_fields.has_key(fieldname)
        # print(type(hasinstance))
        try:
            # 判断列表是否为空，若为空，抛出异常
            if not hasfield:
                raise (core.others.custom_exception.Dada_noexactfiled_exception(fieldname))
        except core.others.custom_exception.Dada_noexactfiled_exception, x:
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
        # 循环判断表单模板的“HasInstance”字段是否为True,若为真，则有表单有实例
        else:
            # 成功获取表单列表数据，返回JSON格式源
            return all_fields[fieldname]['Value']



    #获取实体的指定可修改字段
    def get_fields_reviseexact(self,fieldname):
        all_fields = self.get_fields_revise()
        hasfield=all_fields.has_key(fieldname)
        try:
            # 判断列表是否为空，若为空，抛出异常
            if not hasfield:
                raise (core.others.custom_exception.Dada_noexactfiled_exception(fieldname))
        except core.others.custom_exception.Dada_noexactfiled_exception, x:
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
        # 循环判断表单模板的“HasInstance”字段是否为True,若为真，则有表单有实例
        else:
            # 成功获取表单列表数据，返回JSON格式源
            try:
                if all_fields[fieldname]['U'] is not True:
                    raise (core.others.custom_exception.Dada_noauthority_exception(fieldname))
            except core.others.custom_exception.Dada_noauthority_exception,x:
                print '错误类型--->', x.parameter
                print '错误原因--->', x.desc
            else:
                return all_fields[fieldname]['Value']



#
#
# token=Dada_login(conf.CONFIG.USERNAME,conf.CONFIG.PASSWORD,conf.CONFIG.CLIENNT_ID,conf.CONFIG.CLIENT_SECRET)
# fields=Dada_fields(token,'c083025d-c134-4c5c-846c-740af79b360c','af63a31e-ebec-44e0-8e10-07cf60937e79')
# print (fields.get_fields_read())
