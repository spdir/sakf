# -*- coding: utf-8 -*-
import tornado.web, time, functools, logging
from . import session
from sakf.db.model import (sql)


def auth_url(method):
  """
  认证路由访问权限
  :param method:
  :return:
  """

  @functools.wraps(method)
  def wrapper(self, *args, **kwargs):
    try:
      _session_obj = self.session['url']
      _url_path = self.request.path
      _url_path = _url_path[0:-1] if len(_url_path) > 1 \
                                     and _url_path.endswith('/') else _url_path
      if _url_path not in _session_obj:
        self.write("<script>alert('权限不允许')</script>")
        return self.write_error(403)
    except Exception as e:
      logging.error(e)
      return
    return method(self, *args, **kwargs)

  return wrapper


class BaseHandlers(tornado.web.RequestHandler):
  """
  base app
  """

  def _session(self, obj):
    return session.Session(obj)

  def initialize(self):
    self.session = self._session(self)
    self.sql_engine = sql.sql_session()

  def get_current_user(self):
    return self.session['is_login']

  def now_time(self):
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

  def write_error(self, status_code, **kwargs):
    if status_code == 404:
      return self.render('sakf/error.html', msg=":>404 抱歉，您访问的页面不存在.")
    elif status_code == 403:
      return self.render('sakf/error.html', msg=":>403 抱歉，您无权访问该页面.")
    else:
      return self.render('sakf/error.html', msg=":>500 抱歉，服务器出错了.")

  def on_finish(self):
    self.sql_engine.close()
