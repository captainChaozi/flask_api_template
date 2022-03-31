from functools import wraps

from flask import g, request, current_app

from ext import abort
from .ext_init import cache

token_prefix = "huansi:token:"


def auth(func):
    """
    根据token获取用户
    """

    @wraps(func)
    def inner(*args, **kwargs):
        # current_app.logger.debug(request.headers.get('Authorization'))
        if 'Authorization' in request.headers:
            authorization = request.headers.get('Authorization')
            # 后台登录
            token = authorization[7:]
            bearer = authorization[:7]
            # 后台
            if bearer == 'bearer ':
                if token:
                    key = token_prefix + token

                    try:
                        user = cache.get(key)
                    except Exception as e:
                        current_app.logger.error(e)
                        user = None
                    if not user:
                        abort(401, message="用户未登录")
                    g.user = user
                    g.user_id = None
                    return func(*args, **kwargs)

            elif bearer == 'custome':
                if not token:
                    user_id = request.args.get('user_id')
                    if not user_id:
                        abort(401, message="请登录")
                    else:
                        g.user_id = user_id
                else:
                    user_id = authorization[9:]
                    g.user_id = user_id

                return func(*args, **kwargs)
            else:
                abort(403, message="请求非法")
        else:
            abort(401, message="用户未登录")

        return func(*args, **kwargs)

    return inner
