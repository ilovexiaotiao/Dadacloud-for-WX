# -*- coding: utf-8 -*-
import requests
import json
from datetime import datetime

CLIENNT_ID='1812bf31d6e641dfb4a18d66b41e8cfc'
CLIENT_SECRET='25a93e45e1a949edb5cda6125bd823af'
GRANT_TYPE='password'

def dada_accesstoken(username,password):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
         'Content-Type': 'application/x-www-form-urlencoded',
    }
    url='https://api.dadayun.cn/connect/token'
    params={
        'client_id':CLIENNT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type':GRANT_TYPE,
        'username':username,
        'password':password,
    }
    response=requests.post(url=url,data=params,headers=headers)
    result=json.loads(response.text)
    return result
