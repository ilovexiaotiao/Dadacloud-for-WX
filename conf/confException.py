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