# -*- coding: utf-8 -*-
import requests
import json
from datetime import datetime
import time


class Dada_accesstoken(object):
    # 类的初始化
    def __init__(self, username,password,clientid,clientsecret):
        self.username = username
        self.password = password
        self.clientid=  clientid
        self.clientsecret=clientsecret
        self.datetime= time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    def get_response(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        url = 'https://api.dadayun.cn/connect/token'
        params = {
            'client_id': self.clientid,
            'client_secret': self.clientsecret,
            'grant_type': "password",
            'username': self.username,
            'password': self.password,
        }
        response = requests.post(url=url, data=params, headers=headers)
        result = json.loads(response.text)
        return result['access_token'],result['refresh_token']

    def get_token(self):
        return  self.get_response()[0]


    def get_refresh(self):
        return self.get_response()[1]






#a=Dada_accesstoken('userAdmin','Xiaotiao1',CLIENNT_ID,CLIENT_SECRET)

#print(a.get_token(),a.get_refresh(),a.datetime)