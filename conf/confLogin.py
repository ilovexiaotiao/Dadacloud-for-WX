# -*- coding: utf-8 -*-

# 账号信息
LOGIN_PRARM = {
    'clientId': "1812bf31d6e641dfb4a18d66b41e8cfc",
    'clientSecret': "25a93e45e1a949edb5cda6125bd823af",
    'userName': "userAdmin",
    'passWord': "Xiaotiao1",
    'expireSecond': 2592000,
    # 'expireSecond': 3
}


# 获取ACCESSTOKEN的地址
LOGIN_URL = 'https://api.dadayun.cn/connect/token'


# GET请求头文件
LOGIN_HEADERS = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/58.0.3029.110 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded',
            }
