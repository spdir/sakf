# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sakf.conf import globalConfig

_db_conf = globalConfig.config.get('db')
con_data = {
  'user': _db_conf.get('user'),
  'pwd': _db_conf.get('password'),
  'host': _db_conf.get('host', '127.0.0.1'),
  'port': _db_conf.get('port', 3306),
  'db_name': _db_conf.get('db_name', 'sakf')
}
engine = create_engine(
  "mysql+pymysql://{user}:{pwd}@{host}:{port}/{db_name}?charset=utf8".format(**con_data),
  echo=_db_conf.get('logs', True), pool_size=_db_conf.get('pool_size', 10), pool_recycle=3600)


def sql_session():
  """
  数据库连接对象
  :return:
  """
  Session = sessionmaker(bind=engine)
  session = Session()
  return session
