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
CLIENNT_ID='1812bf31d6e641dfb4a18d66b41e8cfc'
CLIENT_SECRET='25a93e45e1a949edb5cda6125bd823af'
USERNAME='userAdmin'
PASSWORD='Xiaotiao1'
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
        url = 'https://api.dadayun.cn/v1/form/templates?limit=50'
        params = {
            'fields': "",
            'filter': "",
            'start': '',
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
        url =  'https://api.dadayun.cn/v1/form/templates/'+moduleid+'/instances'
        params = {
            'keyOption':"",
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
        url = 'https://api.dadayun.cn/v1/form/templates/' + moduleid + '/instances/'+entityid + '?keyOption=Caption'
        params = {
            'keyOption': "Entity",
            'fields': "",
            'containsAuthority':"True"
        }
        response = requests.get(url=url, data=params, headers=headers)
        result = json.loads(response.text)
        return result


token=Dada_accesstoken(USERNAME,PASSWORD,CLIENNT_ID,CLIENT_SECRET)
form=Dada_form(token)
data=form.get_module_total()
data1=form.get_entity_total('57c80ea2-cd30-4cce-9f58-6a25c505cc79')
data2=form.get_entity('57c80ea2-cd30-4cce-9f58-6a25c505cc79','d1dd9137-e8ce-47f5-aed7-40cf1c841794')
print(data2)
