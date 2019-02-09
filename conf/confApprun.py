# -*- coding: utf-8 -*-
import time

# 转换
DateExchange = {
    'Mon':'星期一',
    'Tue':'星期二',
    'Wed':'星期三',
    'Thu':'星期四',
    'Fri':'星期五',
    'Sat':'星期六',
    'Sun':'星期天'
}
LessonField = "d7aa8b5a-71d0-419d-8893-d112ad5ff266"
LessonExchange ={
    '0': 'fca9debf-1408-4873-a6e5-70e9e36a8fd4', # 健身
    '1': 'c3b6a8ab-618b-4328-85b5-16b39e2cd7ec', # 瑜伽
    '2': 'cc5ad31b-3706-48d0-ba17-91c4fc2bb7fb', # 舞蹈
    '3': '409b846e-7111-4799-9a38-324faa0633de', # 动感单车
    # '星期五': 'Fri',
    # '星期六': 'Sat',
    # '星期天': 'Sun'
}

def exchangeweek(date):
    return DateExchange.get(date)

print type(exchangeweek('星期一'))