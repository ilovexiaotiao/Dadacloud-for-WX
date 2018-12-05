# -*- coding: utf-8 -*-
import requests
import json
import time
import conf.CONFIG
import sys
reload(sys)
from core.login.login_dadayun import Dada_login




login=Dada_login(conf.CONFIG.USERNAME,conf.CONFIG.PASSWORD,conf.CONFIG.CLIENNT_ID,conf.CONFIG.CLIENT_SECRET)
print("ID-->"+login.clientid)
print(login.get_token())
print (login.get_refresh())
print(login.refresh_token())
