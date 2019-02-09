# encoding=utf8

import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, make_response, session
# from werkzeug import secure_filename
import urllib, urllib2
import json, os, datetime
# import redis
import collections
from core.login import DadaLogin,DadaToken,DadaLogger,DadaRedis
from core.form import DadaForm,FormEntity,FormFields,FormModule
from conf.confLogin import LOGIN_PRARM
from conf.confRedis import REDIS_PARAM
from conf.confApprun import LessonExchange,LessonField


# 获取课程JSON数据
class Alist(object):
    def __init__(self, index, datas, datelist):
        # 定义顺序字典
        result_sorted = collections.OrderedDict()
        # 定义课程类别序号
        self.index = index
        # 定义课程大类名称
        self.indexname = datas["leibie"]
        # 定义课程大类描述
        self.indexdesc = datas["desc"]
        # print self.indexname
        # 获取大类下的课程明细JSON
        self.result = datas["plan"]
        # key_list = result.keys()
        # key_list.sort()
        # print key_list
        # 参考datalist，生成有序字典
        # result_sort = result_sorted.fromkeys(datelist)
        # print result
        # 循环赋值
        self.datelist = datelist
        # templist=[]
        # for i in range(0, len(self.result)):
        #     # tempindex = datalist.index(result[i]['xingqi'])
        #     if self.result[i]['xingqi'] in datelist:
        #         # print type(result[i]['xingqi'])
        #         # result_sort[datelist[i]] = result.get(datelist[i])
        #         # tempdic[datelist[tempindex]] = result[i]
        #         templist.append(self.result[i])
        # self.result_sorted = templist

    def form_date_dict(self,datevalue):
        tempdic = {}
        templist=[]
        tempdic.fromkeys(datevalue)
        # print tempdic
        for i in range(0, len(self.result)):
            if self.result[i]['xingqiname'] in self.datelist:
                # print type(result[i]['xingqi'])
                # result_sort[datelist[i]] = result.get(datelist[i])
                # tempdic[datevalue[self.datelist.index(self.result[i]['xingqi'])]] = self.result[i]
                self.result[i]['datestring'] = datevalue[self.datelist.index(self.result[i]['xingqiname'])]
                templist.append(self.result[i])
        return templist




class Adate(object):
    def __init__(self):
        self.date = datetime.date.today()

    def time_string(self, i):
        date1 = self.date + datetime.timedelta(days=i)
        # print date1.strftime(
        #     '%a')
        return date1.strftime(
            '%a')

    def date_string(self, i):
        date1 = self.date + datetime.timedelta(days=i)
        return date1.strftime('%m/%d')

    def date_string_chinese(self, i):
        date1 = self.date + datetime.timedelta(days=i)
        return date1.strftime('%m月%d日')


    # 获取日期字典
    def get_date_dict(self):
        dic = collections.OrderedDict()
        list = []
        for i in range(0, 4):
            list.append(self.time_string(i))
            # print self.time_string(i)
        dic.fromkeys(list)
        for i in range(0, len(list)):
            dic[list[i]] = self.date_string(i).decode('utf-8')
        return dic



# 启动Flask总路由器
app = Flask(__name__)
# 引入DadaCloudAPI
login = DadaLogin(
    username=LOGIN_PRARM['userName'],
    password=LOGIN_PRARM['passWord'],
    client=LOGIN_PRARM['clientId'],
    secret=LOGIN_PRARM['clientSecret'])
# 引入Redis服务器
redis = DadaRedis(login,
                  host=REDIS_PARAM['host'],
                  port=REDIS_PARAM['port'],
                  )
# 通过DadaAPI申请访问许可
token = DadaToken(login, redis)
accesstoken = token.insert_token()

# 创建DadaForm实例
form =DadaForm(login,accesstoken)
# 获取Dada数据库课程数值
optionlist=['0','1','2','3']
datalist =[]
for i in range(0,len(optionlist)):
    fields = FormFields(form, LessonField, LessonExchange[optionlist[i]])
    data = fields.get_fields_list()
    datalist.append(data)
# print data['plan']
# app.secret_key = 'test_session'

@app.route('/lesson_list', methods=['POST', 'GET'])
def get_list():
    # session.clear()
    # 获取课程session
    # for i in range(0,len(optionlist)):
        # session[optionlist[i]] = datalist[i]
        # print session[optionlist[i]]
    # session['0'] = None
    # session['1'] = None
    # session['2'] = None
    # session['3'] = None
    if request.method == 'POST':
        strings = request.get_json()
        indexname = strings['index']
        dates = Adate()
        datedict = dates.get_date_dict()
        datelist = datedict.keys()
        datevalue = datedict.values()
        # print datevalue
        # if session.get(indexname) is None:
        #     print "new"
        #     fields = FormFields(form, LessonField, LessonExchange[indexname])
        data = datalist[int(indexname)]
        # else:
        #     # print session.get(indexname)
        #     data = session.get(indexname)
        #     print "old"

        # print datelist
        # fields = FormFields(form, LessonField, LessonExchange[indexname])
        # data=fields.get_fields_list()
        alist = Alist(indexname, data, datelist)
        result_list = alist.form_date_dict(datevalue)
        # print list.result_sorted
        resp = make_response()
        resp.status_code = 200
        resp.headers["content-type"] = "text/html"
        resp.response = render_template('lesson_list_content.html', result=result_list, indexname=alist.indexname,
                                        desc=alist.indexdesc, datedict=datedict)
        # print resp.response
        # return jsonify(list.result)
        return resp
    else:
        # sorted_result = sorted(data.items(), key=lambda x: x[1], reverse=False)
        fields = FormFields(form, LessonField, LessonExchange['0'])
        data = fields.get_fields_list()
        sorted_result = data['plan']
        # sorted_result = sorted_result[0][1]["plan"]
    return render_template('lesson_list.html', result=sorted_result)

@app.route('/store_map')
def store_map():
    return render_template('store_map.html')


@app.route('/store_desc')
def store_desc():
    return render_template('store_desc.html')


@app.route('/lesson_desc')
def lesson_desc():
    return render_template('lesson_desc.html')


@app.route('/teacher_desc')
def teacher_desc():
    return render_template('teacher_desc.html')


@app.route('/lesson_detail')
def lesson_detail():
    return render_template('lesson_detail.html')


@app.route('/lesson_all')
def lesson_all():
    templist = []
    for i in range(0,4):
        templist.append(datalist[i]['plan'])

    return render_template('lesson_index_new.html', result=templist)

    # return render_template('1111.html', result=templist)



    # return render_template('lesson_index_new.html')


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True)
