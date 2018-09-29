# -*- coding: utf-8 -*-
# Group
from sakf.app.sakf import base
import json, logging
from sakf.utils.sql_page_query import limitQuery
from sakf.db.model import Auth


class GroupHandler(base.BaseHandlers):

  def get(self, suburl, *args, **kwargs):
    return self.write('group')

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
    return_data = {
      "code": 1,
      "msg": "ERROR",
      "count": 1,
      "data": []
    }
    _data = []
    if _name:
      _query_info = limitQuery(Auth.AuthGroup, int(_page), int(_limit), is_filter=True,
                               _filter=Auth.AuthGroup.name.like("%" + _name + "%"))
    else:
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
