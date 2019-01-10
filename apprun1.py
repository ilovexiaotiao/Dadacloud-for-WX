# encoding=utf8

import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, make_response, jsonify
# from werkzeug import secure_filename
import urllib, urllib2
import json, os, datetime
# import redis
import collections

app = Flask(__name__)
path = "E:\Nicholas Shan\sport_coach\static\json\lesson_list1.json"
with open(path, "r") as f:
    # file = file.decode("utf-8-sig")
    data = json.load(f)


# 获取课程JSON数据
class Alist(object):
    def __init__(self, index, datas, datelist):
        # 定义顺序字典
        result_sorted = collections.OrderedDict()
        # 定义课程类别序号
        self.index = index
        # 定义课程大类名称
        self.indexname = datas[index]["name"]
        # 定义课程大类描述
        self.indexdesc = datas[index]["desc"]
        # print self.indexname
        # 获取大类下的课程明细JSON
        result = datas.get(index)["arrange"]
        # key_list = result.keys()
        # key_list.sort()
        # print key_list
        # 参考datalist，生成有序字典
        result_sort = result_sorted.fromkeys(datelist)
        # print result_sort
        # 循环赋值
        for i in range(0, len(datelist)):
            # if datelist[i] in key_list:
            # print key_list[i]
            result_sort[datelist[i]] = result.get(datelist[i])
        # print result_sort
        self.result_sorted = result_sort


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
        return date1.strftime('%m月%d日')

    # 获取日期字典
    def get_date_dict(self):
        dic = collections.OrderedDict()
        list = []
        for i in range(0, 3):
            list.append(self.time_string(i))
        dic.fromkeys(list)
        for i in range(0, len(list)):
            dic[list[i]] = self.date_string(i).decode('utf-8')
        return dic


# datee = Adate()
# datelist=datee.get_date_dict().keys()
# print datelist
# dataa= Alist("1",data,datelist)
# dictt = dataa.result_sorted
# for key,value in dictt.items():
#     for i in value:
#         print i['end']
#
# print dataa.result_sorted.values()


@app.route('/lesson_list', methods=['POST', 'GET'])
def get_list():
    if request.method == 'POST':
        strings = request.get_json()
        indexname = strings['index']
        dates = Adate()
        datedict = dates.get_date_dict()
        datelist = datedict.keys()
        # print datelist
        list = Alist(indexname, data, datelist)
        # print list.result_sorted
        resp = make_response()
        resp.status_code = 200
        resp.headers["content-type"] = "text/html"
        resp.response = render_template('lesson_list_content.html', result=list.result_sorted, indexname=list.indexname,
                                        desc=list.indexdesc, datedict=datedict)
        # print resp.response
        # return jsonify(list.result)
        return resp
    else:
        sorted_result = sorted(data.items(), key=lambda x: x[1], reverse=False)
        sorted_result = sorted_result[0][1]["arrange"]
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


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True)
