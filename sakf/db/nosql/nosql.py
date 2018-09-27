# -*- coding: utf-8 -*-
from sakf.conf import globalConfig
import jdb2

def nosqlDB():
  """
  creat nodb db obj
  :return:
  """
  _nosql_conf = globalConfig.config.get('nodb')
  _nosqlFile = _nosql_conf.get('file')
  _dump_time = _nosql_conf.get('dump_time')
  _dump = _nosql_conf.get('dump', False)
  noSql = jdb2.NoSql(dump=_dump, nosqlFile=_nosqlFile, dumpTime=_dump_time)
  return noSql