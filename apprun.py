# -*- coding: utf-8 -*-
import requests
import json
from flask import Flask, render_template, request,redirect,url_for

from core.login.login_dadayun import Dada_accesstoken
from core.form.get_form import Dada_form
from datetime import datetime

CLIENNT_ID='1812bf31d6e641dfb4a18d66b41e8cfc'
CLIENT_SECRET='25a93e45e1a949edb5cda6125bd823af'
USERNAME='userAdmin'
PASSWORD='Xiaotiao1'


token=Dada_accesstoken(USERNAME,PASSWORD,CLIENNT_ID,CLIENT_SECRET)
form=Dada_form(token)



app = Flask(__name__)
@app.route('/',methods = ['POST', 'GET'])
def initial():
    return "ABC"


@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'GET':
        data = form.get_module_hasinstance()
        return render_template("test.html", result=data)
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        moduleid = data['moduleid']
    # data=form.get_entity_total('e91542af-f10b-47ef-84c6-8537566830fa')
    return redirect(url_for('result1', moduleid=moduleid))



@app.route('/result/<moduleid>',methods = ['POST', 'GET'])
def result1(moduleid):
    data = form.get_entity_total(moduleid)
    if request.method == 'GET':
        return render_template("test1.html", result=data)
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        entityid = data['entityid']
    # data=form.get_entity_total('e91542af-f10b-47ef-84c6-8537566830fa')
    return redirect(url_for('result2', moduleid=moduleid,entityid=entityid))



@app.route('/result/<moduleid>/<entityid>', methods=['POST', 'GET'])
def result2(moduleid,entityid):
    data = form.get_entity(moduleid,entityid)
    if request.method == 'GET':
        return render_template("test2.html", result=data)


if __name__ == '__main__':
    app.run(debug = True)