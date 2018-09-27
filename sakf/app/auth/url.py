# -*- coding: utf-8 -*-
# Url
from sakf.app.sakf import base
from sakf.utils.sql_page_query import limitQuery
from sakf.db.model import (Auth)
import logging, json


class UrlHandler(base.BaseHandlers):

  def get(self, suburl, *args, **kwargs):
    return self.render('auth/urls.html')

  def post(self, suburl, *args, **kwargs):
    try:
      return_data = 'Error'
      if hasattr(self, '_' + suburl):
        func = getattr(self, '_' + suburl)
        return_data = func(self, args, kwargs)
      else:
        return self.render('auth/urls.html')
    except Exception as e:
      logging.error(e)
    return self.write(return_data)

  def _query(self, *args, **kwargs):
    """
    数据查询
    :param args:
    :param kwargs:
    :return:
    """
    return_data = {
      "code": 1,
      "msg": "ERROR",
      "count": 1,
      "data": []
    }
    _data = []
    _page = self.get_argument('page', 1)
    _limit = self.get_argument('limit', 30)
    _query_info = limitQuery(Auth.AuthUrl, int(_page), int(_limit))
    return_data['count'] = _query_info.get('count', 1)
    for _n, _row in enumerate(_query_info.get('data'), 1):
      _tmp_data = {
        'id': _n,
        'uid': _row.id,
        'name': _row.name,
        'url': _row.url
      }
      _data.append(_tmp_data)
    return_data['data'] = _data
    return_data['code'] = 0
    return return_data

  def _modify(self, *args, **kwargs):
    """
    表数据修改
    :param args:
    :param kwargs:
    :return:
    """
    _data = self.get_argument('info', None)
    if _data:
      _data = json.loads(_data)
      self.sql_engine.query(Auth.AuthUrl).filter_by(id=_data.get('uid')).update({
        'name': _data.get('name'),
        'url': _data.get('url')
      })
      self.sql_engine.commit()
    return ''

  def _del(self, *args, **kwargs):
    """
    表单行数据删除
    :param args:
    :param kwargs:
    :return:
    """
    _data = self.get_argument('info', None)
    if _data:
      _data = json.loads(_data)
      self.sql_engine.query(Auth.AuthUrl).filter_by(id=_data.get('uid')).delete()
      self.sql_engine.commit()
    return ''
