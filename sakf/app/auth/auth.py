# -*- coding: utf-8 -*-
# 登陆/登出
from sakf.app.sakf import base
import time, json, logging
from sakf.utils import md5_encryption
from sakf.db.model import Auth


class LoginHandler(base.BaseHandlers):

  def get_user_url(self, group_id):
    """
    获取用户的所有可访问的url
    :param username:
    :return:
    """
    _query_data = self.sql_engine.query(Auth.AuthGroup).filter_by(id=group_id).first().url_route
    _url_id_list = [int(i) for i in _query_data.split(',') if i]
    _url_query_data = self.sql_engine.query(Auth.AuthUrl).filter(Auth.AuthUrl.id.in_(_url_id_list)).all()
    url_list = [url_obj.url for url_obj in _url_query_data]
    return url_list if url_list else []

  def get(self, *args, **kwargs):
    if self.session['is_login']:
      return self.redirect('/')
    next_url = self.get_argument('next', '/')
    return self.render('auth/login.html', next_url=next_url)

  def post(self, *args, **kwargs):
    if self.session['is_login']:
      return self.redirect('/')
    next_url = self.get_argument('next', '/')
    username = self.get_argument('username', None)
    password = self.get_argument('password', None)
    status_code = {
      'status': 0,
      'msg': '账号或密码有误',
      'next_url': next_url
    }
    try:
      if username and password:
        db_user_info = self.sql_engine.query(Auth.AuthUser).filter_by(name=username).first()
        # 判断用户是否被锁定
        if not int(db_user_info.lock):
          status_code['msg'] = '账户已被锁定, 请联系管理员'
          return self.write(status_code)
        # 账户正常登陆
        if db_user_info.name == username and \
                db_user_info.password == md5_encryption.md5_string(password):
          self.session['is_login'] = True
          self.session['is_super'] = True if int(db_user_info.super) else False
          try:
            self.session['url'] = self.get_user_url(db_user_info.group_id)
            status_code['status'] = 1
          except AttributeError:
            status_code['msg'] = '账号无任何权限'
            del self.session[None]
        elif db_user_info.name == username:  # 账户登陆异常
          _lock_cookie = json.loads('{}' if not self.get_secure_cookie('_TLU_') else self.get_secure_cookie('_TLU_'))
          _now_user_lock = _lock_cookie.get(username, 1)
          if int(_now_user_lock) > 5:
            self.sql_engine.query(Auth.AuthUser).filter_by(name=username). \
              update({'lock': 0, 'ltime': self.now_time()})
            self.sql_engine.commit()
            status_code['msg'] = '账户已被锁定, 请联系管理员'
          else:
            _lock_cookie[username] = int(_now_user_lock) + 1
            self.set_secure_cookie('_TLU_', json.dumps(_lock_cookie), expires=time.time() + 60 * 5)
    except TabError as e:
      logging.error(e)
    return self.write(status_code)


class LogoutHandler(base.BaseHandlers):
  def get(self, *args, **kwargs):
    self.post()

  def post(self, *args, **kwargs):
    del self.session[None]
    return self.redirect('/login')
