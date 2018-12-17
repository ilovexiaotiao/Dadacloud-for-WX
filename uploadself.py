# encoding=utf8

import os
from flask import Flask, request, redirect, url_for,send_from_directory,render_template,make_response,Response
from werkzeug import secure_filename
import urllib,urllib2
import json
import redis

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['WX_FOLDER']= WX_FOLDER
# app.config['JSON_AS_ASCII'] = False
# app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/getsign', methods=['GET', 'POST'])
# def get_sign():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file and allowed_file(file.filename):
#             filenames = secure_filename(file.filename)
#     #        newfilename=
#     #        print os.path.join(app.config['UPLOAD_FOLDER'])
#     #        print os.path.join(app.config['UPLOAD_FOLDER'], filenames)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filenames))
#
#     #        return redirect(url_for('uploaded_file' , filename=filenames))
#
#     #return '''
#     #<!doctype html>
#     #<title>Upload new File</title>
#     #<h1>Upload new File</h1>
#     #<form action="" method=post enctype=multipart/form-data>
#       #<p><input type=file name=file>
#         # <input type=submit value=Upload>
#     #</form>
#     #'''
#     return render_template('web qr.html')  # homepage.html在templates文件夹下
#
# @app.route('/upload/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)
#
#
#
# @app.route('/kaoqin')
# def kaoqin():
#     return render_template("kaoqin.html")
#
# @app.route('/<filename>')
# def wx_file(filename):
#     return send_from_directory(app.config['WX_FOLDER'],
#                                filename)
# def wxprepare(filename):
#     filename='MP_verify_nJ147hN15d55YxhL.txt'
#     return redirect(url_for('wx_file' , filename=filename))
#
# @app.route('/',methods=['GET', 'POST'])
# def getCode():
#     #if request.method == 'POST':
#      #   get_sign()
#     #用户同意授权，获取code。通过微信服务器返回的code来获取
#     code = request.args.get('code')
#     #code不为空进行操作
#     if code:
#         print  url_for('uploaded_file', filename='')
#         #获取accessToken和openID
#         openid = ""
#         access_token = ""
#         accessToken = urllib2.Request(url_code.format(appid=appID, appsecret=AppSecret, code=code))
#         res_data = urllib2.urlopen(accessToken)
#         res = res_data.read().decode('utf-8')
#         res_json = json.loads(res)  # 转成json
#         access_token = res_json["access_token"]
#         openid = res_json["openid"]
#         print openid
#         print access_token
# #        r.setex('wx:ACCESS_TOKEN', ACCESS_TOKEN, 7200)
#         #refresh_token=res_json["refresh_token"]
#         #刷新access_token（可写可不写）
#         #getRefreshToken= urllib2.Request(url_retoken.format(appid=appID,refresh_token=refresh_token))
#         #res_data = urllib2.urlopen(getRefreshToken)
#         #res_reToken = res_data.read().decode('utf-8')
#         #res_json = json.loads(res_reToken)  # 转成json
#         #access_token = res_json["access_token"]
#         #r.setex('wx:ACCESS_TOKEN', ACCESS_TOKEN, 7200)  # 将获取到的 ACCESS_TOKEN 存入redis中并且设置过期时间为7200s
#         #获取用户基本信息
#         getUserInfo = urllib2.Request(url_info.format(access_token=access_token,openid=openid))
#         res_data = urllib2.urlopen(getUserInfo)
#         res = res_data.read().decode('utf-8')
#         #返回的结果输入到网页
#         userdic=json.loads(res)
#         nickname=userdic['nickname']
#         userid=userdic['openid']
#     #print nickname
#     #print userid
#
#         response = make_response(redirect(url_for("get_sign")))
#         response.set_cookie('nickname', nickname)
#         response.set_cookie('userid', userid)
#         #return redirect(url_for("get_sign"))
#         return response

#def get__token():
#    access_token = r.get('wx:ACCESS_TOKEN') # 从redis中获取ACCESS_TOKEN
#    if access_token:
#        return access_token
#    try:

#        return access_token, openid
 #   except Exception as e:
 #       return  e

data = {
    "20181214": {
        "name": "瑜伽",
        "desc": "45分钟|舞蹈|免费",
        "arrange": {
            "20181214": [{
                "start": "16:00",
                "end": "17:00",
                "teacher": "高中华",
                "type": "瑜伽老师",
                "url": "",
                    },
                    {
                "start": "16:00",
                "end": "17:00",
                "teacher": "高中华",
                "type": "瑜伽老师",
                "url": "",
                    },
                ],

            "20181215": [{
                "date": "12月14日",
                "start": "16:00",
                "end": "17:00",
                "teacher": "刘中华",
                "type": "瑜伽老师",
                "url": ""
            },
                {
                    "date": "12月14日",
                    "start": "16:00",
                    "end": "17:00",
                    "teacher": "王中华",
                    "type": "瑜伽老师",
                    "url": ""
                }
            ],
        },
    },

    "20181215": {
        "name": "交谊舞",
        "desc": "45分钟|舞蹈|免费",
        "arrange": {
            "20181214": [{
                "date": "12月14日",
                "start": "16:00",
                "end": "17:00",
                "teacher": "高中华1",
                "type": "舞蹈老师",
                "url": ""
            },
                {
                    "date": "12月14日",
                    "start": "16:00",
                    "end": "17:00",
                    "teacher": "高中华1",
                    "type": "舞蹈老师",
                    "url": ""
                }
            ],
            "20181215": [{
                "date": "12月14日",
                "start": "16:00",
                "end": "17:00",
                "teacher": "刘中华1",
                "type": "舞蹈老师",
                "url": ""
            },
                {
                    "date": "12月14日",
                    "start": "16:00",
                    "end": "17:00",
                    "teacher": "王中华1",
                    "type": "舞蹈老师",
                    "url": ""
                }
            ]

        }
    }
}
class Alist(object):
    def __init__(self):
        self.index =""
        self.result = sorted(data.items(), key=lambda x: x[1], reverse=False)

    def setvalue(self,value):
        self.index = value
        return list.index

list = Alist()

@app.route('/lesson_list/get',methods = ['POST'])
def set_index():
    # list = Alist()
    strings = request.get_json()
    list.index = strings['index']
    list.result = data.get(list.index)["arrange"]
    return list.index

@app.route('/lesson_list/get',methods = ['GET'])
def get_index():
    # list = Alist()
    # strings = request.get_json()
    # list.index = strings['index']
    # list.result = data.get(list.index)["arrange"]
    print list.index
    print list.result
    return render_template('aaa.html',result= list.result,index = list.index )


@app.route('/lesson_list',methods = ['POST', 'GET'])
def get_list():
    list=Alist()
    if request.method == 'POST':
        strings = request.get_json()
        list.index = strings['index']
        list.result =data.get(list.index)["arrange"]
        return list.index
    else:
        sorted_result = sorted(data.items(), key=lambda x: x[1], reverse=False)
        sorted_result = sorted_result[0][1]["arrange"]
    print list.index
    return render_template('lesson_list.html',result= sorted_result,index = list.index )





if __name__ == "__main__":
    app.run(debug=True)
    #app.run(debug=True)