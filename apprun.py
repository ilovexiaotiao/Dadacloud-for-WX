# -*- coding: utf-8 -*-
import requests
import json
from flask import Flask, render_template, request

from core.login.login_dadayun import Dada_accesstoken
from core.form.get_form import Dada_form
from datetime import datetime

CLIENNT_ID='1812bf31d6e641dfb4a18d66b41e8cfc'
CLIENT_SECRET='25a93e45e1a949edb5cda6125bd823af'
USERNAME='userAdmin'
PASSWORD='Xiaotiao1'


token=Dada_accesstoken(USERNAME,PASSWORD,CLIENNT_ID,CLIENT_SECRET)
form=Dada_form(token)
data=form.get_module_hasinstance()

app = Flask(__name__)
@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'GET':
        return render_template("test.html",result = data)


if __name__ == '__main__':
    app.run(debug = True)