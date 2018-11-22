# -*- coding: utf-8 -*-
import requests
import json
from flask import Flask, render_template, request
from core.login.login_dadayun import Dada_accesstoken
from datetime import datetime

FILEDS =""
FILTER =""
START =""
LIMIT =""
SORT =""
COUNT =""

class Dada_form(object):
    def __init__(self,token):
        if not isinstance(token,Dada_accesstoken):
            raise Exception("not must type")
        self.accesstoken=token.get_token()
        self.refreshtoken=token.get_refresh()
        self.clientid=token.clientid
        self.username=token.username
        self.datetime=token.datetime
        self.headers= {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        #'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + self.accesstoken
        }

    def get_module_total(self):
        headers = self.headers
        url = 'https://api.dadayun.cn/v1/form/templates'
        params = {
            'fields': "",
            'filter': "",
            'start': "",
            'limit': "",
            'sort': "",
            'count': ""
        }
        response = requests.get(url=url, data=params, headers=headers)
        result = json.loads(response.text)
        return result


    def get_module_hasinstance(self):
        a=self.get_module_total()
        result=[]
        for i in range(0,len(a)-1):
            if a[i]['HasInstance'] is True:
                result.append(a[i])
        return result


    def get_module_content(self,moduleid):
        headers = self.headers
        url = 'https://api.dadayun.cn/v1/form/templates/'+moduleid
        params = {
            'version': "",
            }
        response = requests.get(url=url, data=params, headers=headers)
        result = json.loads(response.text)
        return result


    def get_entity_total(self,moduleid):
        headers = self.headers
        url =  'https://api.dadayun.cn/v1/form/templates/'+moduleid+'/instance'
        params = {
            'keyOpition':"",
            'fields': "",
            'filter': "",
            'start': "",
            'limit': "",
            'sort': "",
            'count': ""
        }
        response = requests.get(url=url, data=params, headers=headers)
        result = json.loads(response.text)
        return result

    def get_entity(self,moduleid,entityid):
        headers = self.headers
        url = 'https://api.dadayun.cn/v1/form/templates/' + moduleid + '/instance/'+entityid
        params = {
            'keyOpition': "",
            'fields': "",
            'containsAuthority':"True"
        }
        response = requests.get(url=url, data=params, headers=headers)
        result = json.loads(response.text)
        return result



