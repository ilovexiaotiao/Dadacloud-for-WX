# -*- coding: utf-8 -*-
import requests
import json
from login import DadaLogin ,DadaToken
import conf.confForm
from exception import LoginException, TypeException, EmptyException,Dada_notcorrectparam_exception,Dada_noexactfiled_exception,Dada_noauthority_exception


# 搭搭云图表模板类：
# 1，此流程获取token适合开发者没有自己的web服务器，且应用为原生程序，即客户端应用（同时应用无法与浏览器交互，但是可以外调用浏览器）
# 2，需先完成Access_Token验证，才可以进行表单操作。
# 搭搭云图表实体类：
# 1，此流程获取token适合开发者没有自己的web服务器，且应用为原生程序，即客户端应用（同时应用无法与浏览器交互，但是可以外调用浏览器）
# 2，需先完成模板定义验证，才可以进行表单操作。
# 3，分为两大模块，查询模块，通过GET形式，推送Access_Token和相应字段到API平台，返回JSON数据。
# 4，操作模块，通过POST、DELETE形式，推送Access_Token和相应JSON数据到API平台，返回提示信息。
# 搭搭云图表字段类：
# 1，此流程获取token适合开发者没有自己的web服务器，且应用为原生程序，即客户端应用（同时应用无法与浏览器交互，但是可以外调用浏览器）
# 2，需先完成实体定义验证，才可以进行表单操作。
# 3，可以根据用户权限，获取具体字段。
# 4，通过GET形式，推送Access_Token和相应字段到API平台，返回JSON数据。

class DadaForm(object):
    #类的初始化
    def __init__(self,login,accesstoken):
        # 定义当前用户的Logger类
        self.logger = login.logger
        # DadaForm类的失效期
        self.initialTime = login.initialTime
        # self.expireTimeStruct = login.expireTimeStruct
        self.expireTime = login.expireTime
        self.accesstoken = accesstoken
        #初始判断token参数是否为Dada_token类
        try:
            # 判断login是否为DadaLogin类
            intype_login = isinstance(login, DadaLogin)
            if not intype_login:
                raise (
                    TypeException(
                        'not_login_type'))
            # 调用表单错误类，查看错误日志
        except TypeException as a:
            # 打印 TypeException错误日志
            self.logger.log_typeexception(a)
        else:
            # 初始赋值
            self.accesstoken = accesstoken
            # self.accesstoken = 'bf95f8c8cf18454779c4f2bc2a426cc01f69009536c4aea83cb2c2046a5278e8'


class FormModule(object):
    # 类的初始化
    def __init__(self,dadaform):
        self.form = dadaform
        self.accesstoken = dadaform.accesstoken
        self.logger = dadaform.logger
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            # 'Content-Type': 'application/x-www-form-urlencoded',
            # 采用表头传参方式，将Access_Token发送至API平台
            'Authorization': 'Bearer ' + self.accesstoken
        }
        self.paramsstr = '?limit=' + conf.confForm.MODULE_PARAMS['limit']\
                    + '&fields=' + conf.confForm.MODULE_PARAMS['fields'] \
                    + '&filter=' + conf.confForm.MODULE_PARAMS['filter'] \
                    + '&sort=' + conf.confForm.MODULE_PARAMS['sort'] \
                    + '&count=' + conf.confForm.MODULE_PARAMS['count']
        self.url = 'https://api.dadayun.cn/v1/form/templates' +self.paramsstr


    def get_module_list(self,page = 0,hasinstance=1):
        if page > 0:
            url = self.url +  '&start=' + str(page-1)
        else:
            url = self.url
        try:
            # 发送GET请求
            response = requests.get(url=url, headers=self.headers)
            # result_totalcount = json.loads(json.dumps(dict(response.headers)))
            result_modulelist = json.loads(response.content)
            # 获取当前Response的状态码
            httpcode = response.status_code
            # 打印LoginException错误日志
            self.logger.log_http_response(httpcode)
            # 判断返回结果中是否有错误提示
            # if 'error' in result_refresh:
            #     raise (
            #         LoginException(
            #             result_refresh['error']))
            if type(result_modulelist) is dict:
                raise (Dada_notcorrectparam_exception(result_modulelist))
        # 调用登录错误类，查看错误日志
        except EmptyException as x:
            self.logger.log_loginexception(x)
        # 成功更新Access_Token和Refresh_Token
        else:
            if hasinstance == 1:
                result_hasinstance=[]
                inlen = len(result_modulelist)
                for i in range(0, inlen):
                    if result_modulelist[i]['HasInstance'] is True and result_modulelist[i]['Status'] > 0:
                        result_hasinstance.append(result_modulelist[i])
                return result_hasinstance
            else:
                return result_modulelist



class FormEntity(object):
    #类的初始化
    def __init__(self, dadaform,moduleid):
        self.form = dadaform
        self.accesstoken = dadaform.accesstoken
        self.logger = dadaform.logger
        self.moduleid=moduleid
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            # 'Content-Type': 'application/x-www-form-urlencoded',
            # 采用表头传参方式，将Access_Token发送至API平台
            'Authorization': 'Bearer ' + self.accesstoken
        }
        self.paramsstr = '?limit=' + conf.confForm.MODULE_ENTITY_PARAMS['limit'] \
                         + '&fields=' + conf.confForm.MODULE_ENTITY_PARAMS['fields'] \
                         + '&filter=' + conf.confForm.MODULE_ENTITY_PARAMS['filter'] \
                         + '&sort=' + conf.confForm.MODULE_ENTITY_PARAMS['sort'] \
                         + '&count=' + conf.confForm.MODULE_ENTITY_PARAMS['count']\
                         + '&keyOption' + conf.confForm.MODULE_ENTITY_PARAMS['keyOption']
        self.url = 'https://api.dadayun.cn/v1/form/templates/' +  self.moduleid + '/instances' + self.paramsstr

    def get_entity_list(self,page = 0, submit=1):
        if page > 0:
            url = self.url +  '&start=' + str(page-1)
        else:
            url = self.url
        try:
            # 发送GET请求
            response = requests.get(url=url, headers=self.headers)
            # result_totalcount = json.loads(json.dumps(dict(response.headers)))
            result_modulelist = json.loads(response.content)
            # 获取当前Response的状态码
            httpcode = response.status_code
            # 打印LoginException错误日志
            self.logger.log_http_response(httpcode)
            # 判断返回结果中是否有错误提示
            # if 'error' in result_refresh:
            #     raise (
            #         LoginException(
            #             result_refresh['error']))
            if type(result_modulelist) is dict:
                raise (Dada_notcorrectparam_exception(result_modulelist))
        # 调用登录错误类，查看错误日志
        except EmptyException as x:
            self.logger.log_loginexception(x)
        # 成功更新Access_Token和Refresh_Token
        else:
            if submit == 1:
                result_submit=[]
                inlen = len(result_modulelist)
                for i in range(0, inlen):
                    if result_modulelist[i]['IsValid'] is True:
                        result_submit.append(result_modulelist[i])
                return result_submit
            else:
                return result_modulelist


    #通过MODULE_ID，获取指定单据模板
    def get_entity_fields(self):
        result_fields_show=[]
        paramsstr = '?version=' + conf.confForm.MODULE_ID_PARAMS['version']
        # 合成GET形式URL
        url = 'https://api.dadayun.cn/v1/form/templates/'+self.moduleid + paramsstr
        #print url
        # 将上述参数发送至API平台，获取指定表单模板
        try:
            # 发送GET请求
            response = requests.get(url=url, headers=self.headers)
            # result_totalcount = json.loads(json.dumps(dict(response.headers)))
            result_entityfields = json.loads(response.content)
            # 获取当前Response的状态码
            httpcode = response.status_code
            # 打印LoginException错误日志
            self.logger.log_http_response(httpcode)
            # 判断返回结果中是否有错误提示
            # if 'error' in result_refresh:
            #     raise (
            #         LoginException(
            #             result_refresh['error']))
            if  result_entityfields.has_key('Message'):
                #print "OK"
                raise (Dada_notcorrectparam_exception(result_entityfields))
        # 调用登录错误类，查看错误日志
        except EmptyException as x:
            self.logger.log_loginexception(x)
        # 成功更新Access_Token和Refresh_Token
        else:
            #print result_entityfields
            nohidden = result_entityfields['Fields']
            # 成功获取实体字段数据
            for i in range( 0 , len(nohidden)):
                if nohidden[i]['Hidden'] is not True:
                     result_fields_show.append(nohidden[i])
            # 生成新的字典，装在可读字段列表
            #print result_fields_show
            #print len(result_fields_show)
        return result_fields_show

    def get_entity_fields_name(self):
        all_fields=self.get_entity_fields()
        #print all_fields[0]
        inlen=len(all_fields)
        #print inlen
        result_name=[]
        #从实体内容中提取实体名称，并以列表形式输出
        for i in range(1,inlen):
            result_name.append(all_fields[i]['EntityPropertyName'])
        return result_name




class FormFields(object):
    #类的初始化
    def __init__(self, dadaform, moduleid, entityid):
        self.form = dadaform
        self.accesstoken = dadaform.accesstoken
        self.logger = dadaform.logger
        self.moduleid = moduleid
        self.entityid = entityid
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            # 'Content-Type': 'application/x-www-form-urlencoded',
            # 采用表头传参方式，将Access_Token发送至API平台
            'Authorization': 'Bearer ' + self.accesstoken
        }
        self.paramsstr = '?keyOption=' + conf.confForm.MODULE_ENTITY_ID_PARAMS['keyOption'] \
                    + '&fields=' + conf.confForm.MODULE_ENTITY_ID_PARAMS['fields'] \
                    + '&containsAuthority=' + conf.confForm.MODULE_ENTITY_ID_PARAMS['containsAuthority']
        self.url = 'https://api.dadayun.cn/v1/form/templates/' + self.moduleid + '/instances/' + self.entityid + self.paramsstr


    #获取实体的所有字段
    def get_fields_list(self,canread=1,fieldname=None):
        try:
            # 发送GET请求
            response = requests.get(url=self.url, headers=self.headers)
            # result_totalcount = json.loads(json.dumps(dict(response.headers)))
            result_allfields = json.loads(response.content)
            # 获取当前Response的状态码
            httpcode = response.status_code
            # 打印LoginException错误日志
            self.logger.log_http_response(httpcode)
            # 判断返回结果中是否有错误提示
            # if 'error' in result_refresh:
            #     raise (
            #         LoginException(
            #             result_refresh['error']))
            if result_allfields.has_key('error'):
                raise (Dada_notcorrectparam_exception(result_allfields['error']))
        # 调用登录错误类，查看错误日志
        except EmptyException as x:
            self.logger.log_loginexception(x)
        # 成功更新Access_Token和Refresh_Token
        else:
            if canread==1:
                result_canread = {}
                key_list = []
                for key, value in result_allfields.items():
                    if type(value) is not dict:
                        # 第一种情况，返回正常值，计入可读列表
                        key_list.append(key)
                    else:
                        # 第二种情况，返回字典值，计入可读列表
                        if result_allfields[key]['R'] is True:
                            key_list.append(key)
                # 生成新的字典，装在可读字段列表
                result_canread = result_canread.fromkeys(key_list)
                # 循环赋值
                for key, value in result_canread.items():
                    result_canread[key] = result_allfields[key]
                return result_canread
            else:
                result_canrevise = {}
                key_list = []
                for key, value in result_allfields.items():
                    if type(value) is not dict:
                        # 第一种情况，返回正常值，计入可读列表
                        key_list.append(key)
                    else:
                        # 第二种情况，返回字典值，计入可读列表
                        if result_allfields[key]['U'] is True:
                            key_list.append(key)
                # 生成新的字典，装在可修改字段列表
                result_canrevise = result_canrevise.fromkeys(key_list)
                # 循环赋值
                for key, value in result_canrevise.items():
                    result_canrevise[key] = result_allfields[key]
                return result_canrevise


    #获取实体的指定可读字段
    def get_fields_name(self,fieldname,canread = 1):
        if canread ==1:
            all_fields = self.get_fields_list()
            hasfield=all_fields.has_key(fieldname)
            # print(type(hasinstance))
            try:
                # 判断列表是否为空，若为空，抛出异常
                if not hasfield:
                    raise (Dada_noexactfiled_exception(fieldname))
            except Dada_noexactfiled_exception, x:
                print '错误类型--->', x.parameter
                print '错误原因--->', x.desc
            # 循环判断表单模板的“HasInstance”字段是否为True,若为真，则有表单有实例
            else:
                # 成功获取表单列表数据，返回JSON格式源
                return all_fields[fieldname]['Value']
        else:
            all_fields = self.get_fields_list(canread=0)
            hasfield = all_fields.has_key(fieldname)
            try:
                # 判断列表是否为空，若为空，抛出异常
                if not hasfield:
                    raise (Dada_noexactfiled_exception(fieldname))
            except Dada_noexactfiled_exception, x:
                print '错误类型--->', x.parameter
                print '错误原因--->', x.desc
            # 循环判断表单模板的“HasInstance”字段是否为True,若为真，则有表单有实例
            else:
                # 成功获取表单列表数据，返回JSON格式源
                try:
                    if all_fields[fieldname]['U'] is not True:
                        raise (Dada_noauthority_exception(fieldname))
                except Dada_noauthority_exception, x:
                    print '错误类型--->', x.parameter
                    print '错误原因--->', x.desc
                else:
                    return all_fields[fieldname]['Value']






