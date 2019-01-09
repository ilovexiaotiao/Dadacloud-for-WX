# -*- coding: utf-8 -*-

#配置信息
#获取MODULE_LIST模板配置信息
MODULE_PARAMS = {
            'fields': "",           #返回字段，fields允许包含的字段：Id, Name, CreatorName, Status, HasInstance, CreateTime, TplType。默认值为空，返回所有字段。
            'filter': "",           #筛选条件，	筛选条件，目前只支持按单据名称模糊搜索；
            'start': '0',           #页码，0-2147483647范围内某个整数值，默认值为0。
            'limit': '20',         #每页显示记录条数，0-2147483647范围内某个整数值，默认值为20。
            'sort': "-CreateTime",              #排序方法，可选字段：Name, Status, CreateTime, TplType。默认值为-CreateTime。
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
            'limit': '20',  # 每页显示记录条数，0-2147483647范围内某个整数值，默认值为20。
            'sort': "-CreateTime",  # 排序方法，可选字段：Name, Status, CreateTime, TplType。默认值为-CreateTime。
            'count': "true"  # 是否包含总记录数
        }
#获取指定MODULE_ID指定ENTITY_ID的实体配置信息
MODULE_ENTITY_ID_PARAMS = {
    'keyOption': "Entity",#提交的实例数据和返回的实例数据以什么为属性名（键名）。- Entity 以实体属性名为属性名；- Caption 以[组名-]控件名为属性名；- Id 以字段的Id为属性名；- FieldName 以字段的FieldName为属性名，默
    'fields': "", # 返回字段，fields允许包含的字段：Id, Name, CreatorName, Status, HasInstance, CreateTime, TplType。默认值为空，返回所有字段。
    'containsAuthority': "false" #containsAuthority=true，也可不带（不带默认containsAuthority=true）。
}

#上传实体模板配置信息
MODULE_ENTITY_SEND_PARAMS = {
    'keyOption': "Entity",#提交的实例数据和返回的实例数据以什么为属性名（键名）。- Entity 以实体属性名为属性名；- Caption 以[组名-]控件名为属性名；- Id 以字段的Id为属性名；- FieldName 以字段的FieldName为属性名，默
    'IsSubmit': "true", # 返回字段，fields允许包含的字段：Id, Name, CreatorName, Status, HasInstance, CreateTime, TplType。默认值为空，返回所有字段。
    'containsAuthority': "false", #containsAuthority=true，也可不带（不带默认containsAuthority=true）。
    'AutoFillMode':"forceempty"#新建的单据实例数据是否需后台完成自动填充： - 默认空为不填充； - forceempty填充空值（客户端未提交的或提交的值为空）；- forceall填充所有（即使客户端提交上来有值）； - forceautocode只填充关联了自动编码的字段。
}
