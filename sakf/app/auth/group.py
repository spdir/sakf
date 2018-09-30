# -*- coding: utf-8 -*-
# Group
import json
import logging
from sakf.utils.sql_page_query import limitQuery
from sakf.db.model import Auth
from sakf.app.sakf import base
import tornado.web


class GroupHandler(base.BaseHandlers):

  @base.auth_url
  @tornado.web.authenticated
  def get(self, suburl, *args, **kwargs):
    return self.render('auth/group.html')

  @base.auth_url
  @tornado.web.authenticated
  def post(self, suburl, *args, **kwargs):
    return_data = {}
    try:
      if hasattr(self, '_' + suburl):
        func = getattr(self, '_' + suburl)
        return_data = func(self, args, kwargs)
      else:
        return self.render('auth/group.html')
    except Exception as e:
      logging.error(e)
    return self.write(return_data)

  def _add(self, *args, **kwargs):
    """
    添加
    :param args:
    :param kwargs:
    :return:
    """
    status = 0
    _info = json.loads(self.get_argument('info', None))
    _group_name = _info.get('name')
    if _group_name:
      if not self.sql_engine.query(Auth.AuthGroup).filter_by(name=_group_name).first():
        _obj = Auth.AuthGroup(name=_group_name)
        self.sql_engine.add(_obj)
        self.sql_engine.commit()
        if self.sql_engine.query(Auth.AuthGroup).filter_by(name=_group_name).first():
          status = 1
      else:
        status = 2
    return {'status': status}

  def _del(self, *args, **kwargs):
    """
    删除
    :param args:
    :param kwargs:
    :return:
    """
    _info = json.loads(self.get_argument('info', None))
    _group_id = _info.get('uid', None)
    _group_obj = self.sql_engine.query(Auth.AuthGroup).filter_by(id=int(_group_id))
    if _group_obj.first():
      _user_obj = self.sql_engine.query(Auth.AuthUser).filter_by(group_id=int(_group_id)).update(
        {'group_id': 2}
      )
      _group_obj.delete()
      self.sql_engine.commit()
    return ''

  def _modify(self, *args, **kwargs):
    """
    修改
    :param args:
    :param kwargs:
    :return:
    """
    return_data = {'status': 0}
    _tp = self.get_argument('tp', None)
    _info = json.loads(self.get_argument('info', None))
    if _tp == 'name':  # 修改组名
      _name = _info.get('name', None)
      _name_obj = self.sql_engine.query(Auth.AuthGroup).filter_by(id=int(_info.get('uid')))
      if _name_obj.first():
        _name_obj.update({'name': _name})
        self.sql_engine.commit()
    elif _tp == 'url':  # 删除一个组权限
      _group_id = _info.get('uid')
      _url_id = _info.get('url_id')
      if _group_id:
        _group_obj = self.sql_engine.query(Auth.AuthGroup).filter_by(id=int(_group_id))
        _old_route = _group_obj.first().url_route
        _url_id_list = [i for i in _old_route.split(',') if i]
        _url_id_list.remove(str(_url_id))
        _group_obj.update({
          'url_route': ','.join(_url_id_list)
        })
        self.sql_engine.commit()
    return return_data

  def _query(self, *args, **kwargs):
    """
    查询
    :param args:
    :param kwargs:
    :return:
    """
    _name = self.get_argument('name', None)
    _page = self.get_argument('page', 1)
    _limit = self.get_argument('limit', 30)
    _tp = self.get_argument('tp', None)
    return_data = {
      "code": 1,
      "msg": "ERROR",
      "count": 1,
      "data": []
    }
    _data = []
    if _name:  # 组名模糊匹配
      _query_info = limitQuery(Auth.AuthGroup, int(_page), int(_limit), is_filter=True,
                               _filter=Auth.AuthGroup.name.like("%" + _name + "%"))
    elif _tp == 'url':  # 根据组id获取当前组的url权限
      _group_id = self.get_argument('group_id', None)
      _group_obj = self.sql_engine.query(Auth.AuthGroup).filter_by(id=int(_group_id))
      _url_id_list = [int(i) for i in _group_obj.first().url_route.split(',') if i]
      _all_url_obj = self.sql_engine.query(Auth.AuthUrl).filter(Auth.AuthUrl.id.in_(_url_id_list)).all()
      __url_data = []
      _tmp_return_data = {
        "code": 1,
        "msg": "ERROR",
        "count": 1,
        "data": []
      }
      for _n, _row in enumerate(_all_url_obj, 1):
        _tmp_url_data = {
          'id': _n,
          'uid': _row.id,
          'name': _row.name,
          'url': _row.url
        }
        __url_data.append(_tmp_url_data)
      _tmp_return_data['data'] = __url_data
      _tmp_return_data['code'] = 0
      return _tmp_return_data
    else:  # 无过滤条件查询
      _query_info = limitQuery(Auth.AuthGroup, int(_page), int(_limit))
    return_data['count'] = _query_info.get('count', 1)
    for _n, _row in enumerate(_query_info.get('data'), 1):
      _tmp_data = {
        'id': _n,
        'uid': _row.id,
        'name': _row.name
      }
      _data.append(_tmp_data)
    return_data['data'] = _data
    return_data['code'] = 0
    return return_data
