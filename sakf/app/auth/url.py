# -*- coding: utf-8 -*-
# Url
import json
import logging
from sqlalchemy import and_
import tornado.web
from sakf.app.sakf import base
from sakf.utils.sql_page_query import limitQuery
from sakf.db.model import (Auth)


class UrlHandler(base.BaseHandlers):

  @base.auth_url
  @tornado.web.authenticated
  def get(self, suburl, *args, **kwargs):
    return self.render('auth/urls.html')

  @base.auth_url
  @tornado.web.authenticated
  def post(self, suburl, *args, **kwargs):
    return_data = {}
    try:
      if hasattr(self, '_' + suburl):
        func = getattr(self, '_' + suburl)
        return_data = func(self, args, kwargs)
      else:
        return self.render('auth/urls.html')
    except Exception as e:
      logging.error(e)
    return self.write(return_data)

  def _add(self, *args, **kwargs):
    """
    添加URL
    :param args:
    :param kwargs:
    :return:
    """
    status = 0

    def disUrl(url):
      """
      处理url
      :param url:
      :return:
      """
      if url.endswith('/') and len(url) > 1:
        url = url[0:-1]
      return url

    try:
      _info = self.get_argument('info', None)
      if _info:
        _info = json.loads(_info)
        _name, _url = _info.get('name'), disUrl(_info.get('url'))
        if not self.sql_engine.query(Auth.AuthUrl).filter_by(name=_name).first() and \
                not self.sql_engine.query(Auth.AuthUrl).filter_by(url=_url).first():
          _obj = Auth.AuthUrl(name=_name, url=_url)
          self.sql_engine.add(_obj)
          self.sql_engine.commit()
          if self.sql_engine.query(Auth.AuthUrl).filter(
                  Auth.AuthUrl.name == _name and Auth.AuthUrl.url == _url).first():
            status = 1
          try:
            self.__admin_add_url(_name)  # 管理源添加此权限
          except:
            pass
        else:
          status = 2
    except AttributeError:
      pass
    return {'status': status}

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

  def _query(self, *args, **kwargs):
    """
    数据查询
    :param args:
    :param kwargs:
    :return:
    """
    _name = self.get_argument('name', None)
    _url = self.get_argument('url', None)
    _page = self.get_argument('page', 1)
    _limit = self.get_argument('limit', 30)
    return_data = {
      "code": 1,
      "msg": "ERROR",
      "count": 1,
      "data": []
    }
    _data = []
    if _url or _name:
      if _url and not _name:  # url或name模糊匹配
        filter = Auth.AuthUrl.url.like("%" + _url + "%")
      elif _name and not _url:
        filter = Auth.AuthUrl.name.like("%" + _name + "%")
      else:
        filter = and_(Auth.AuthUrl.name.like("%" + _name + "%"), Auth.AuthUrl.url.like("%" + _url + "%"))
      _query_info = limitQuery(Auth.AuthUrl, int(_page), int(_limit), is_filter=True, _filter=filter)
    else:  # 无过滤条件查询
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

  def __admin_add_url(self, url_name):
    """
    添加url后admin组自动添加url
    :param url_name:
    :return:
    """
    _url_id = self.sql_engine.query(Auth.AuthUrl).filter_by(name=url_name).first().id
    _group_obj = self.sql_engine.query(Auth.AuthGroup).filter_by(id=1)
    _old_route = _group_obj.first().url_route
    _url_id_list = [i for i in _old_route.split(',') if i]
    _url_id_list.append(str(_url_id))
    _group_obj.update({
      'url_route': ','.join(_url_id_list)
    })
    self.sql_engine.commit()
