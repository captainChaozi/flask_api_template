import datetime
import logging
from sqlalchemy import Integer, DateTime, Date, DECIMAL
from flask import abort as original_flask_abort
from flask import request, g, current_app
from werkzeug.exceptions import HTTPException

logger = logging.getLogger('abort')


def remove_spaces(s):
    s = str(s)
    if not (s.startswith(' ') or s.endswith(' ') or s.startswith('\u3000') or s.endswith('\u3000')):
        return s
    s = s.strip(' ')
    s = s.strip('\u3000')
    return remove_spaces(s)


def check_param(value, _type):
    if isinstance(_type, Date):
        try:
            value = datetime.datetime.strptime(value, '%Y-%m-%d')
        except (ValueError, TypeError):
            abort(400, message="时间参数不正确")
    elif isinstance(_type, DateTime):
        if len(value) == 10:
            try:
                value = datetime.datetime.strptime(value, '%Y-%m-%d')
            except (ValueError, TypeError):
                abort(400, message="时间参数不正确")
        elif len(value) == 19:
            try:
                value = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                abort(400, message="时间参数不正确")
        else:
            abort(400, message="时间参数不正确")
    elif isinstance(_type, (Integer, DECIMAL)):
        try:
            value = float(value)
        except (ValueError, TypeError):
            abort(400, message="数字参数不正确")
    else:
        value = str(value)
    return value


def param_query(models, param=None, like_fields=(), between_field=(), in_field=()):
    param = dict(param)
    param_list = []
    for model in models:
        for k, v in param.items():
            if getattr(model, k, None):
                if k in like_fields:
                    param_list.append(getattr(model, k).like('%{}%'.format(remove_spaces(v))))
                elif k in in_field:
                    param_list.append(getattr(model, k).in_(v if isinstance(v, list) else [v]))
                else:
                    param_list.append(getattr(model, k) == v)
        for i in between_field:
            start = i + '_start'
            end = i + '_end'
            print(param)
            if (start in param) and (end in param) and getattr(model, i, None):
                if start.find('time') != -1 and end.find('time') != -1:
                    start = datetime.datetime.strptime(param.get(start), '%Y-%m-%d %H:%M:%S')
                    end = datetime.datetime.strptime(param.get(end), "%Y-%m-%d %H:%M:%S")
                elif start.find('data') != -1 and end.find('data') != -1:
                    start = datetime.datetime.strptime(param.get(start), '%Y-%m-%d')
                    end = datetime.datetime.strptime(param.get(end), "%Y-%m-%d") + datetime.timedelta(days=1)
                else:
                    start = param.get(start)
                    end = param.get(end)
                print(start, end)
                param_list.append(getattr(model, i).between(start, end))

    return tuple(param_list)


def paginator(query, schema):
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 10)
    pagination = query.paginate(page=int(page), per_page=int(per_page), error_out=False)
    total_number = pagination.total  # 获取总条数
    items = pagination.items  # 获取数据
    result = schema.dump(items)
    return {
        'data': result,
        'paging': {'page': int(page),
                   'per_page': int(per_page),
                   'total_number': int(total_number)}
    }


def abort(http_status_code, **kwargs):
    """
    来自于flask_restful 只有在flask_restful的框架中才起作用
    :param http_status_code:
    :param kwargs:
    :return:
    """
    try:
        original_flask_abort(http_status_code)
    except HTTPException as e:
        if len(kwargs):
            e.data = kwargs
            current_app.logger.error(kwargs)
        raise


def soft_delete(model, ids):
    db_session = g.db_session
    if not isinstance(ids, list):
        ids = [ids]
    ins = db_session.query(model).filter(model.id.in_(ids),).all()
    if not ins:
        abort(400, message="删除的资源不存在")
    for i in ins:
        i.is_delete = 1
        i.save(db_session)
    return None


def real_delete(model, ids):
    db_session = g.db_session
    if not isinstance(ids, list):
        ids = [ids]
    db_session.query(model).filter(model.id.in_(ids)).delete(synchronize_session=False)
    return None
