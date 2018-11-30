# -*- coding: utf-8 -*-
import requests
import json
from flask import Flask, render_template, request,redirect,url_for
import threading
from core.login.login_dadayun import Dada_login
from core.form.get_module import Dada_module
from core.form.get_entity import Dada_entity
from core.form.get_fields import Dada_fields
import conf.CONFIG
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


token = Dada_login(conf.CONFIG.USERNAME, conf.CONFIG.PASSWORD, conf.CONFIG.CLIENNT_ID,
                   conf.CONFIG.CLIENT_SECRET)

app = Flask(__name__)
@app.route('/',methods = ['POST', 'GET'])
def module_list():
    moduleid=''
    module=Dada_module(token)
    if request.method == 'GET':
        data = module.get_module_list_all()
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
    entity=Dada_entity(token.get_token(),moduleid)
    data = entity.get_entity_list()
    if request.method == 'GET':
        return render_template("test1.html", result=data)
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        entityid = data['entityid']
    # data=form.get_entity_total('e91542af-f10b-47ef-84c6-8537566830fa')
    return redirect(url_for('result2', entityid=entityid))



@app.route('/<moduleid>/<entityid>', methods=['POST', 'GET'])
def fields_list(moduleid,entityid):
    fields=Dada_fields(token.get_token(),moduleid,entityid)
    data = fields.get_fields_all()
    if request.method == 'GET':
        return render_template("test2.html", result=data)



if __name__ == '__main__':
    app.run()