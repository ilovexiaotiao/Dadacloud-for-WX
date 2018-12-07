# -*- coding: utf-8 -*-
import requests
import json
from flask import Flask, render_template, request
from core.login.login_dadayun import Dada_token
import conf.CONFIG
import core.others.custom_exception


# 搭搭云图表模板类：
# 1，此流程获取token适合开发者没有自己的web服务器，且应用为原生程序，即客户端应用（同时应用无法与浏览器交互，但是可以外调用浏览器）
# 2，需先完成Access_Token验证，才可以进行表单操作。


class Dada_module(object):
    #类的初始化
    def __init__(self,token):
        #初始判断token参数是否为Dada_token类
        try:
            self.token = token
            intype=isinstance(self.token,Dada_token)
            if not intype:
                raise (core.others.custom_exception.Dada_notcorrecttype_exception(self.token))
            # 调用表单错误类，查看错误日志
        except core.others.custom_exception.Dada_notcorrecttype_exception , a:
            print '错误概述--->', a
            print '错误类型--->', a.parameter
            print '错误原因--->', a.desc
        else:
            # 初始赋值
            self.accesstoken = token.get_token()
            # self.accesstoken = 'bf95f8c8cf18454779c4f2bc2a426cc01f69009536c4aea83cb2c2046a5278e8'

    def  get_module_totalcount(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            # 'Content-Type': 'application/x-www-form-urlencoded',
            # 采用表头传参方式，将Access_Token发送至API平台
            'Authorization': 'Bearer ' + self.accesstoken
        }
        paramsstr = '?limit=' + str(1)\
                    + '&fields=' + conf.CONFIG.MODULE_PARAMS['fields'] \
                    + '&filter=' + conf.CONFIG.MODULE_PARAMS['filter'] \
                    + '&start=' + str(0) \
                    + '&sort=' + conf.CONFIG.MODULE_PARAMS['sort'] \
                    + '&count=' + conf.CONFIG.MODULE_PARAMS['count']

        # 合成GET形式URL
        url = 'https://api.dadayun.cn/v1/form/templates' + paramsstr

        # 将上述参数发送至API平台，获取表单模板列表
        try:
            response = requests.get(url=url, headers=headers)
            # 从HEADER部分提取总记录数
            result_totalcount = json.loads(json.dumps(dict(response.headers)))
            # print type(result_totalcount)
            # print (type(result))
            if type(result_totalcount) is not dict:
                raise (core.others.custom_exception.Dada_emptylist_exception(type(result_totalcount)))
        # 调用参数错误类，查看错误日志
        except core.others.custom_exception.Dada_notcorrectparam_exception, x:
            print '错误概述--->', x
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
        # 成功获取表单列表数据，返回JSON格式源
        else:
            return result_totalcount['Total-Count']

    def get_module_list_all(self):
        # API平台报送表头、URL与参数
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            # 'Content-Type': 'application/x-www-form-urlencoded',
            # 采用表头传参方式，将Access_Token发送至API平台
            'Authorization': 'Bearer ' + self.accesstoken
        }
        totalcount=self.get_module_totalcount()
        paramsstr = '?limit=' + str(totalcount) \
                    + '&fields=' + conf.CONFIG.MODULE_PARAMS['fields'] \
                    + '&filter=' + conf.CONFIG.MODULE_PARAMS['filter'] \
                    + '&start=' + str(0) \
                    + '&sort=' + conf.CONFIG.MODULE_PARAMS['sort'] \
                    + '&count=' + conf.CONFIG.MODULE_PARAMS['count']

        # 合成GET形式URL
        url = 'https://api.dadayun.cn/v1/form/templates' + paramsstr

        # 将上述参数发送至API平台，获取表单模板列表
        try:
            response = requests.get(url=url, headers=headers)
            # 从HEADER部分提取总记录数
            module_totalcount = response.headers['Total-Count']
            result_modulelist = json.loads(response.content)
            # print (type(result))
            if type(result_modulelist) is dict:
                raise (core.others.custom_exception.Dada_notcorrectparam_exception(result_modulelist))
        # 调用参数错误类，查看错误日志
        except core.others.custom_exception.Dada_notcorrectparam_exception, x:
            print '错误概述--->', x
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
        # 成功获取表单列表数据，返回JSON格式源
        else:
            # if result_modulelist['count']==0:
            #     return ""
            # else:
            return result_modulelist

    #获取所有的表单模板列表
    def get_module_list_index(self,page):
        #获取列表页码数
        index=page-1
        # API平台报送表头、URL与参数
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            # 'Content-Type': 'application/x-www-form-urlencoded',
            # 采用表头传参方式，将Access_Token发送至API平台
            'Authorization': 'Bearer ' + self.accesstoken
        }
        paramsstr=     '?limit='+conf.CONFIG.MODULE_PARAMS['limit']\
                    + '&fields='+conf.CONFIG.MODULE_PARAMS['fields']\
                    + '&filter='+conf.CONFIG.MODULE_PARAMS['filter'] \
                    + '&start=' + str(index)\
                    + '&sort=' + conf.CONFIG.MODULE_PARAMS['sort'] \
                    + '&count=' + conf.CONFIG.MODULE_PARAMS['count']

        #合成GET形式URL
        url = 'https://api.dadayun.cn/v1/form/templates'+paramsstr

        # 将上述参数发送至API平台，获取表单模板列表
        try:
            response = requests.get(url=url, headers=headers)
            #从HEADER部分提取总记录数
            # self.totalcount = response.headers['Total-Count']
            result_modulelist = json.loads(response.content)
            #print (type(result))
            if type(result_modulelist) is dict:
                raise (core.others.custom_exception.Dada_notcorrectparam_exception(result_modulelist))
        #调用参数错误类，查看错误日志
        except core.others.custom_exception.Dada_notcorrectparam_exception,x:
            print '错误概述--->', x
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
        #成功获取表单列表数据，返回JSON格式源
        else:
            # if result_modulelist['count']==0:
            #     return ""
            # else:
            return result_modulelist




    #获取带有实例的表单模板列表
    def get_module_list_hasinstance_all(self):
        #先获取所有表单模板
        hasinstance=self.get_module_list_all()
        result_hasinstance=[]
        #print(type(hasinstance))
        try:
            #判断列表是否为空，若为空，抛出异常
            if hasinstance is None:
                raise (core.others.custom_exception.Dada_emptylist_exception(hasinstance))
        except core.others.custom_exception.Dada_emptylist_exception,x:
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
        #循环判断表单模板的“HasInstance”字段是否为True,若为真，则有表单有实例
        else:
            # 成功获取表单列表数据，返回JSON格式源
            inlen = len(hasinstance)
            for i in range(0, inlen):
                if hasinstance[i]['HasInstance'] is True and hasinstance[i]['Status']>0 :
                    result_hasinstance.append(hasinstance[i])
            return result_hasinstance

    #获取带有实例的表单模板列表
    def get_module_list_hasinstance_index(self,page):
        #先获取所有表单模板
        hasinstance=self.get_module_list_index(page)
        result_hasinstance=[]
        #print(type(hasinstance))
        try:
            #判断列表是否为空，若为空，抛出异常
            if hasinstance is None:
                raise (core.others.custom_exception.Dada_emptylist_exception(hasinstance))
        except core.others.custom_exception.Dada_emptylist_exception,x:
            print '错误类型--->', x.parameter
            print '错误原因--->', x.desc
        #循环判断表单模板的“HasInstance”字段是否为True,若为真，则有表单有实例
        else:
            # 成功获取表单列表数据，返回JSON格式源
            inlen = len(hasinstance)
            for i in range(0, inlen):
                if hasinstance[i]['HasInstance'] is True and hasinstance[i]['Status']>0 :
                    result_hasinstance.append(hasinstance[i])
            return result_hasinstance




