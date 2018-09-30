# -*- coding: utf-8 -*-
from sqlalchemy import func
from sakf.db.model.sql import sql_session

sql_session = sql_session()


def limitQuery(obj, now_page, page_limit, is_filter=False, _filter=None):
  """
  简单单表查询
  :param obj: 要查询的表对象
  :param now_page: 当前页
  :param page_limit: 每页多少条
  :param filter: 过滤条件，默认None
  :return: dict
  """
  if is_filter:
    count = sql_session.query(func.count(obj.id)).filter(_filter).scalar()
    data = sql_session.query(obj).filter(_filter).limit(page_limit).offset((now_page - 1) * page_limit).all()
  else:
    count = sql_session.query(func.count(obj.id)).scalar()
    data = sql_session.query(obj).limit(page_limit).offset((now_page - 1) * page_limit).all()
  sql_session.close()
  return_data = {
    'count': count,
    'data': data
  }
  return return_data
