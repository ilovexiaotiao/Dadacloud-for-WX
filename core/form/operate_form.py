# -*- coding: utf-8 -*-
import requests
import json
from flask import Flask, render_template, request

from core.login.login_dadayun import dada_accesstoken
from core.form.get_form import dada_form_module
from datetime import datetime

KEPOPTHIN=""
FILEDS =""
FILTER =""
START =""
LIMIT =""
SORT =""
COUNT =""


def dada_form_module(accesstoken,module_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        #'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer ' + accesstoken
    }

    url='https://api.dadayun.cn/v1/form/templates/'+module_id +'/instances'
    params={
        'keyOption':"",
        'fields':"",
        'filter':"" ,
        'start':"",
        'limit':"",
        'sort':"",
        'count':""
    }
    response=requests.get(url=url,data=params,headers=headers)
    result=json.loads(response.text)
    return result


key=dada_accesstoken("userAdmin","Xiaotiao1")
access_token = key["access_token"]
print(access_token)
key2=dada_form_module(access_token)
# 从字典里取 data 数组
dataList = key2[1]
print dataList

app = Flask(__name__, template_folder='../templates',static_folder="",static_url_path="")
@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'GET':
        return render_template("test.html",result = dataList)


if __name__ == '__main__':
    app.run(debug = True)