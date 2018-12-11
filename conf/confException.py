# -*- coding: utf-8 -*-

# 错误描述集合
LOGIN_ERRORS = {
    'invalid_request': '请求不合法',
    'invalid_client': 'client_id或client_secret参数无效',
    'invalid_grant': '提供的凭证验证失败',
    'unauthorized_client': '客户端没有权限',
    'unsupported_grant_type': '不支持的 GrantType',
    'invalid_scope': 'Scope验证失败',
    'temporarily_unavailable': '服务暂时无法访问',
    'server_error': '服务器内部错误，请联系管理员',
    'expire_error': 'LOGIN类已失效，请重新创建'
}

TYPE_ERRORS = {
    'not_login_type': '变量并非DadaLogin类',
    'not_redis_type': '变量并非DadaRedis类',
    'not_token_type': '变量并非DadaToken类',
    'not_from_type': '变量并非DadaFrom类',
    'not_log_type': '变量并非DadaLog类',
    'not_operate_type': '变量并非DadaOperate类',
    'temporarily_unavailable': '服务暂时无法访问',
    'server_error': '服务器内部错误，请联系管理员',
    'expire_error': 'LOGIN类已失效，请重新创建'


}

EMPTY_ERRORS = {
    'function_return_empty': '函数返回值为None',
    'redis_key_empty': 'Redis中指定Key值的Value为None',
    'dict_key_empty': '提供的凭证验证失败',
    'list_empty': '客户端没有权限',
    'dict_empty': '不支持的 GrantType',
    'param_empty': 'Scope验证失败',
    'temporarily_unavailable': '服务暂时无法访问',
    'server_error': '服务器内部错误，请联系管理员',
    'expire_error': 'LOGIN类已失效，请重新创建'
}
