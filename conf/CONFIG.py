# -*- coding: utf-8 -*-

#配置信息
#获取MODULE_LIST模板配置信息
MODULE_PARAMS = {
            'fields': "",           #返回字段，fields允许包含的字段：Id, Name, CreatorName, Status, HasInstance, CreateTime, TplType。默认值为空，返回所有字段。
            'filter': "",           #筛选条件，	筛选条件，目前只支持按单据名称模糊搜索；
            'start': '0',           #页码，0-2147483647范围内某个整数值，默认值为0。
            'limit': '100',         #每页显示记录条数，0-2147483647范围内某个整数值，默认值为20。
            'sort': "",              #排序方法，可选字段：Name, Status, CreateTime, TplType。默认值为-CreateTime。
            'count': "true"         #是否包含总记录数
        }
#获取ENTITY_FIELDS模板配置信息
MODULE_ID_PARAMS = {
             'version': "-1",          #	版本号，0-2147483647范围内某个整数值。- -1 总是返回，默认值；- 大于-1：    - 如果前端版本提交的版本和服务器端版本相同，返回空；  - 否则返回新版本的单据模板。
        }
#获取指定ENTITY实体列表配置信息
MODULE_ENTITY_PARAMS = {
            'keyOption': "Caption", #提交的实例数据和返回的实例数据以什么为属性名（键名）。- Entity 以实体属性名为属性名；- Caption 以[组名-]控件名为属性名；- Id 以字段的Id为属性名；- FieldName 以字段的FieldName为属性名，默认。
            'fields': "",  # 返回字段，fields允许包含的字段：Id, Name, CreatorName, Status, HasInstance, CreateTime, TplType。默认值为空，返回所有字段。
            'filter': "",  # 筛选条件，	筛选条件，目前只支持按单据名称模糊搜索；
            'start': '0',  # 页码，0-2147483647范围内某个整数值，默认值为0。
            'limit': '100',  # 每页显示记录条数，0-2147483647范围内某个整数值，默认值为20。
            'sort': "",  # 排序方法，可选字段：Name, Status, CreateTime, TplType。默认值为-CreateTime。
            'count': "true"  # 是否包含总记录数
        }
#获取指定MODULE_ID指定ENTITY_ID的实体配置信息
MODULE_ENTITY_ID_PARAMS = {
    'keyOption': "Entity",#提交的实例数据和返回的实例数据以什么为属性名（键名）。- Entity 以实体属性名为属性名；- Caption 以[组名-]控件名为属性名；- Id 以字段的Id为属性名；- FieldName 以字段的FieldName为属性名，默
    'fields': "", # 返回字段，fields允许包含的字段：Id, Name, CreatorName, Status, HasInstance, CreateTime, TplType。默认值为空，返回所有字段。
    'containsAuthority': "True" #containsAuthority=true，也可不带（不带默认containsAuthority=true）。
}

#print MODULE_PARAMS['limit']


#账号信息
CLIENNT_ID='1812bf31d6e641dfb4a18d66b41e8cfc'       #客户ID
CLIENT_SECRET='25a93e45e1a949edb5cda6125bd823af'    #客户secret
USERNAME='userAdmin'                                    #管理员ID
PASSWORD='Xiaotiao1'                                    #管理员PWD



#其他信息

# 错误描述集合
LOGIN_ERRORS = {
    'invalid_request': '请求不合法',
    'invalid_client': 'client_id或client_secret参数无效',
    'invalid_grant': '提供的凭证验证失败',
    'unauthorized_client': '客户端没有权限',
    'unsupported_grant_type': '不支持的 GrantType',
    'invalid_scope': 'Scope验证失败',
    'temporarily_unavailable': '服务暂时无法访问',
    'server_error': '服务器内部错误，请联系管理员'
}
