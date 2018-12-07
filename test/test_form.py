# -*- coding: utf-8 -*-
import conf.CONFIG
import conf.CONFIG_REDIS
import time
from core.login.login_dadayun import Dada_token,Dada_login
from core.others.save_redis import Dada_redis
from core.form.get_module import Dada_module
from core.form.get_entity import Dada_entity
from core.form.get_fields import Dada_fields

def output_form(module,entity,field):

    print "测试结果如下："
    print "--------------MODULE类------------------------"
    print "ACCESSTOKEN-->" + module.accesstoken
    print "总记录数-->" + str(module.totalcount)
    print "第一页记录数-->" + str(len(module.get_module_list_index(1)))
    print "第一页记录数(有实例）-->" + str(len(module.get_module_list_hasinstance_index(1)))
    print "第一页内容（有实例）-->"
    for i in range(0, len(module.get_module_list_hasinstance_index(1))):
        count = i + 1
        print "record" + str(count)
        print module.get_module_list_hasinstance_index(1)[i]
    print "--------------ENTITY类------------------------"
    print "ACCESSTOKEN-->" + entity.accesstoken
    print "总记录数-->" + str(entity.totalcount)
    print "第一页记录数(已提交）-->" + str(len(entity.get_entity_list_submit_index(1)))
    print "第一页内容（已提交）-->"
    for i in range(0, len(entity.get_entity_list_submit_index(1))):
        count = i + 1
        print "record" + str(count)
        print entity.get_entity_list_submit_index(1)[i]
    print "第一页记录数(未提交）-->" + str(len(entity.get_entity_list_revise_index(1)))
    print "第一页内容（未提交）-->"
    for i in range(0, len(entity.get_entity_list_revise_index(1))):
        count = i + 1
        print "record" + str(count)
        print entity.get_entity_list_revise_index(1)[i]
    print "当前实体的字段属性-->"
    for key in entity.get_entity_fields():
        print key
    print "--------------FIELD类------------------------"
    print "ACCESSTOKEN-->" + entity.accesstoken
    for key, value in field.get_fields_read().items():
        print key, value

def count_time(second):
    for i in range(0,second):
        second_count=i+1
        print "-----counting second-----:"+str(second_count)
        time.sleep(second)



login = Dada_login(conf.CONFIG.USERNAME,conf.CONFIG.PASSWORD,conf.CONFIG.CLIENNT_ID,conf.CONFIG.CLIENT_SECRET)
redis=Dada_redis(host=conf.CONFIG_REDIS.REDIS_HOST,port=conf.CONFIG_REDIS.REDIS_PORT)
token = Dada_token(login,redis)
module=Dada_module(token)
entity=Dada_entity(token,'57c80ea2-cd30-4cce-9f58-6a25c505cc79')
field=Dada_fields(token,'57c80ea2-cd30-4cce-9f58-6a25c505cc79','d1dd9137-e8ce-47f5-aed7-40cf1c841794')
output_form(module,entity,field)


