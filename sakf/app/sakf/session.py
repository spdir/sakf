# -*- coding: utf-8 -*-
# 内存session

import time
from sakf.db.nosql import nosql

# 初始化NoSQL DB
_nosql = nosql.nosqlDB()
session = _nosql.createDB('session')


class Session():
  """
  memory session
  """

  def __init__(self, handler):
    self.handler = handler
    self.random_index_str = self.handler.get_secure_cookie('_token_sson_', None)
    self.random_time_str = self.handler.get_secure_cookie('_tson_', None)
    self.random_str = '| m | z | c |'
    if self.random_index_str and not self.random_time_str:
      tmp = None
      if isinstance(self.random_index_str, bytes):
        tmp = self.random_index_str.decode()
      session.dropKey(tmp)
      self.random_index_str = None
    elif self.random_time_str and not self.random_index_str:
      tmp = None
      if isinstance(self.random_time_str, bytes):
        tmp = self.random_time_str.decode()
      session.dropKey(tmp)
      self.random_time_str = None

  def __get_random_str(self):
    import hashlib, time
    md = hashlib.md5()
    md.update(bytes(str(time.time()) + self.random_str, encoding='utf-8'))
    return md.hexdigest()

  def __setitem__(self, key, value):
    if not self.random_index_str and not self.random_time_str:
      self.random_index_str = self.__get_random_str()
      self.random_time_str = self.random_index_str
    else:
      if isinstance(self.random_index_str, bytes):
        self.random_index_str = self.random_index_str.decode()
      if isinstance(self.random_time_str, bytes):
        self.random_time_str = self.random_time_str.decode()
      if self.random_index_str not in session.getKeys() and \
              self.random_time_str not in session.getKeys():
        self.random_index_str = self.__get_random_str()
        self.random_time_str = self.random_index_str
    session.createTable(self.random_index_str).setValue(key, value)
    self.handler.set_secure_cookie("_token_sson_", self.random_index_str, expires_days=None)
    self.handler.set_secure_cookie('_tson_', self.random_index_str, expires=time.time() + 3 * 60 ** 2)

  def __getitem__(self, key):
    if isinstance(self.random_index_str, bytes):
      self.random_index_str = self.random_index_str.decode()
    if isinstance(self.random_time_str, bytes):
      self.random_time_str = self.random_time_str.decode()
    if not self.random_index_str and not self.random_time_str:
      return None
    else:
      if self.random_index_str == self.random_time_str:
        current_user = session.getValue(self.random_index_str)
        if not current_user:
          return None
        else:
          return session.createTable(self.random_index_str).getValue(key)
      else:
        return None

  def __delitem__(self, key):
    random_index_str = None
    random_time_str = None
    if isinstance(self.random_index_str, bytes):
      random_index_str = self.random_index_str.decode()
    if isinstance(self.random_time_str, bytes):
      random_time_str = self.random_time_str.decode()
    if key == None or key == '':
      session.dropKey(random_index_str)
      session.dropKey(random_time_str)
      self.handler.clear_cookie("_token_sson_")
      self.handler.clear_cookie('_tson_')
    else:
      if random_index_str:
        session.createTable(random_index_str).dropKey(key)
      elif random_time_str:
        session.createTable(random_time_str).dropKey(key)
