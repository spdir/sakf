# -*- coding: utf-8 -*-
# User
from sakf.app.sakf import base
import logging, json
from sakf.db.model import Auth
from sakf.utils.sql_page_query import limitQuery
from sakf.utils.md5_encryption import md5_string


class UserHandler(base.BaseHandlers):

  def get(self, suburl, *args, **kwargs):
    return self.render('auth/user.html')

  def post(self, suburl, *args, **kwargs):
    return_data = {}
    try:
      if hasattr(self, '_' + suburl):
        func = getattr(self, '_' + suburl)
        return_data = func(self, args, kwargs)
      else:
        return self.render('auth/user.html')
    except Exception as e:
      logging.error(e)
    return self.write(return_data)

  def _add(self, *args, **kwargs):
    """
    添加用户
    :param args:
    :param kwargs:
    :return:
    """
    status = 0
    try:
      _form_info = json.loads(self.get_argument('info', None))
      _username = _form_info.get('name', None)
      _password = _form_info.get('password', None)
      _lock = _form_info.get('lock', 0)
      _group_id = _form_info.get('group', None)
      if _username and _password and _group_id:
        if not self.sql_engine.query(Auth.AuthUser).filter_by(name=_username).first():
          _obj = Auth.AuthUser(
            name=_username,
            password=md5_string(md5_string(_password)),
            super=0,
            lock=int(_lock),
            group_id=int(_group_id),
            ctime=self.now_time(),
            ltime=self.now_time()
          )
          self.sql_engine.add(_obj)
          self.sql_engine.commit()
          if self.sql_engine.query(Auth.AuthUser).filter_by(name=_username).first():
            status = 1
        else:
          status = 2
    except AttributeError:
      pass
    return {'status': status}

  def _del(self, *args, **kwargs):
    """
    删除用户
    :param args:
    :param kwargs:
    :return:
    """
    _form_info = json.loads(self.get_argument('info', None))
    if _form_info:
      self.sql_engine.query(Auth.AuthUser).filter_by(id=_form_info.get('uid')).delete()
      self.sql_engine.commit()
    return ''

  def _modify(self, *args, **kwargs):
    """
    修改用户信息
    :param args:
    :param kwargs:
    :return:
    """
    return_data = {'status': 0}
    _tp = self.get_argument('tp', None)
    _info = json.loads(self.get_argument('info', None))
    if _tp == 'lock':
      _id = _info.get('uid', None)
      _lock_id = self.get_argument('lock', 0)
      self.sql_engine.query(Auth.AuthUser).filter_by(id=_id).update({
        'lock': int(_lock_id),
        'ltime': self.now_time()
      })
      self.sql_engine.commit()
    elif _tp == 'passwd':
      _passwd = _info.get('passwd', None)
      if _passwd:
        self.sql_engine.query(Auth.AuthUser).filter_by(id=int(_info.get('uid'))).update({
          'password': md5_string(md5_string(_passwd))
        })
        self.sql_engine.commit()
        return_data['status'] = 1
    elif _tp == 'name':
      _name = _info.get('name', None)
      if _name:
        if not self.sql_engine.query(Auth.AuthUser).filter_by(name=_name).first():
          self.sql_engine.query(Auth.AuthUser).filter_by(id=int(_info.get('uid'))).update({
            'name': _name
          })
          self.sql_engine.commit()
          return_data['status'] = 1
    elif _tp == 'group':
      _group_id = _info.get('group')
      if _group_id:
        if self.sql_engine.query(Auth.AuthGroup).filter_by(id=int(_group_id)).first():
          self.sql_engine.query(Auth.AuthUser).filter_by(id=int(_info.get('uid'))).update({
            'group_id': int(_group_id)
          })
          self.sql_engine.commit()
          return_data['status'] = 1
          return_data['group'] = self.sql_engine.query(Auth.AuthGroup).filter_by(id=int(_group_id)).first().name
    return return_data

  def _query(self, *args, **kwargs):
    """
    查询
    :param args:
    :param kwargs:
    :return:
    """
    _username = self.get_argument('username', None)
    _page = self.get_argument('page', 1)
    _limit = self.get_argument('limit', 30)
    return_data = {
      "code": 1,
      "msg": "ERROR",
      "count": 1,
      "data": []
    }
    _data = []
    if _username:
      _query_info = limitQuery(Auth.AuthUser, int(_page), int(_limit), is_filter=True,
                               _filter=Auth.AuthUser.name.like("%" + _username + "%"))
    else:
      _query_info = limitQuery(Auth.AuthUser, int(_page), int(_limit))
    return_data['count'] = _query_info.get('count', 1)
    for _n, _row in enumerate(_query_info.get('data'), 1):
      _tmp_data = {
        'id': _n,
        'uid': _row.id,
        'name': _row.name,
        'super': "YES" if _row.super == 1 else "NO",
        'lock': "YES" if _row.lock == 0 else "N0",
        'ctime': str(_row.ctime),
        'ltime': str(_row.ltime),
        'group': self.sql_engine.query(Auth.AuthGroup).filter_by(id=_row.group_id).first().name
      }
      _data.append(_tmp_data)
    return_data['data'] = _data
    return_data['code'] = 0
    return return_data
