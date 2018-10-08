# -*- coding: utf-8 -*-
# global conf
import os

__baseDir__ = os.path.dirname(os.path.dirname(__file__))

config = {
  'bash_dir': __baseDir__,
  'log_file': './logs/sakf.log',
  'encrypt': {
    'certfile': os.path.join(__baseDir__, 'data', 'encrypt', 'server.crt'),
    'keyfile': os.path.join(__baseDir__, 'data', 'encrypt', 'server.key')
  },
  'ssl': {
    'private': os.path.join(__baseDir__, 'data', 'ssl', 'rootCA-key.pem'),
    'pubilc': os.path.join(__baseDir__, 'data', 'ssl', 'rootCA.pem'),
  },
  'db': {
    'host': '127.0.0.1',
    'port': '3306',
    'user': 'root',
    'password': '123.com',
    # 'db_name': 'sakf-demo',
    'db_name': 'sakf-test',
    'pool_size': 100,
    'logs': False
  },
  'nodb': {
    'dump': True,
    'file': os.path.join(__baseDir__, 'db', 'nosql', 'nosql.db'),
    'dump_time': 3
  }
}
