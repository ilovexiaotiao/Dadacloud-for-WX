# -*- coding: utf-8 -*-
import requests
import json
from flask import Flask, render_template, request
import conf.CONFIG,conf.CONFIG_REDIS
from core.others.save_redis import Dada_redis
from core.login.login_dadayun import Dada_login,Dada_token
from core.form.operate_entity import Dada_operate











login = Dada_login(conf.CONFIG.USERNAME,conf.CONFIG.PASSWORD,conf.CONFIG.CLIENNT_ID,conf.CONFIG.CLIENT_SECRET)
redis=Dada_redis(host=conf.CONFIG_REDIS.REDIS_HOST,port=conf.CONFIG_REDIS.REDIS_PORT)
token = Dada_token(login,redis)
tokens=Dada_login(conf.CONFIG.USERNAME,conf.CONFIG.PASSWORD,conf.CONFIG.CLIENNT_ID,conf.CONFIG.CLIENT_SECRET)
form= Dada_operate(tokens,'c083025d-c134-4c5c-846c-740af79b360c')
