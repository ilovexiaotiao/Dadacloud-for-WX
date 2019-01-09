# -*- coding: utf-8 -*-
import requests
import json
from flask import Flask, render_template, request,redirect,url_for,sessions
from core.login import DadaLogin,DadaToken,DadaLogger,DadaRedis
from core.form import DadaForm,FormEntity,FormFields,FormModule
from conf.confLogin import LOGIN_PRARM
from conf.confRedis import REDIS_PARAM


login = DadaLogin(
    username=LOGIN_PRARM['userName'],
    password=LOGIN_PRARM['passWord'],
    client=LOGIN_PRARM['clientId'],
    secret=LOGIN_PRARM['clientSecret'])
redis = DadaRedis(login,
                  host=REDIS_PARAM['host'],
                  port=REDIS_PARAM['port'],
                  )
token = DadaToken(login, redis)
accesstoken = token.insert_token()
form =DadaForm(login,accesstoken)

app = Flask(__name__)
@app.route('/',methods = ['POST', 'GET'])
def module_list():
    moduleid=''
    module=FormModule(form)
    if request.method == 'GET':
        data = module.get_module_list()
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
    entity=FormEntity(form,moduleid)
    data = entity.get_entity_list()
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
    fields=FormFields(form,moduleid,entityid)
    data = fields.get_fields_list()
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