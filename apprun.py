# -*- coding: utf-8 -*-
import requests
import json
from flask import Flask, render_template, request,redirect,url_for,sessions
import threading
from core.others.save_redis import Dada_redis
from core.login.login_dadayun import Dada_login,Dada_token
from core.form.get_module import Dada_module
from core.form.get_entity import Dada_entity
from core.form.get_fields import Dada_fields
from core.form.operate_entity import Dada_operate
import conf.CONFIG,conf.CONFIG_REDIS
from datetime import datetime

# class mythread(threading.Thread):
#     def __init__(self, token, interval):
#         threading.Thread.__init__(self)
#
#         self.token = token
#         self.clientid=token.clientid
#         self.username=token.username
#         self.start=token.start
#         self.end=token.end
#         self.interval = interval
#         self.app=Flask(__name__)
#
#     def run(self):
#         for x in filter(lambda x: x % self.interval == 0, range(10)):
#             self.app.run(debug=True)



app = Flask(__name__)
@app.route('/',methods = ['POST', 'GET'])
def module_list():
    moduleid=''
    module=Dada_module(token)
    if request.method == 'GET':
        data = module.get_module_list_hasinstance_all()
        return render_template("test.html", result=data)
    if request.method == 'POST':
        data = request.get_json()
        #print(data)
        moduleid = data['moduleid']
    # data=form.get_entity_total('e91542af-f10b-47ef-84c6-8537566830fa')
    return redirect(url_for('entity_list',moduleid=moduleid))


#c083025d-c134-4c5c-846c-740af79b360c
#
@app.route('/<moduleid>',methods = ['POST', 'GET'])
def entity_list(moduleid):
    entityid=''
    entity=Dada_entity(token,moduleid)
    data = entity.get_entity_list_submit_all()
    if request.method == 'GET':
        return render_template("test1.html", result=data)
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        entityid = data['entityid']
    # data=form.get_entity_total('e91542af-f10b-47ef-84c6-8537566830fa')
    return redirect(url_for('fields_list', entityid=entityid))



@app.route('/<moduleid>/<entityid>', methods=['POST', 'GET'])
def fields_list(moduleid,entityid):
    fields=Dada_fields(token,moduleid,entityid)
    data = fields.get_fields_read()
    if request.method == 'GET':
        return render_template("test2.html", result=data)


@app.route('/<moduleid>/<entityid>/submit', methods=['POST','GET'])
def fields_submit(moduleid,entityid):
    if request.method == 'GET':
        return render_template("test3.html")
    if request.method == 'POST':
        title = request.form.get('Title')
        field1 = request.form.get('Field1')
        input = request.form.get('input')
        print title, field1, input
        operate=Dada_operate(token,moduleid)
        instancedata={
            "Title": title,
            "Field1": field1,
            "input": input,
        }
        operate.create_entity()
    return redirect(url_for('fields_list', moduleid=moduleid,entityid=entityid))
        #return redirect(url_for('fields_list',moduleid=moduleid,entityid=entityid))


if __name__ == '__main__':
    app.run()