# -*- coding: utf-8 -*-
# import base64, uuid
# base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

import os
import tornado.web
from tornado.options import define, options, parse_config_file
from sakf.conf import globalConfig
from sakf.route import route

_Conf = globalConfig.config
_Base_dir = globalConfig.__baseDir__

# define
define(name='address', default='0.0.0.0', help='listen address')
define(name='port', default=8080, help='listen address', type=int)
define(name='ssl', default=False, help="use ssl", type=bool)


class ServerApp(object):
  """
  Tornado APP Setting
  """

  def __init__(self):
    """
    init param
    """
    self.globalConfig = globalConfig.config
    self.base_dir = os.path.dirname(os.path.dirname(__file__))

  def __tempaltesPath__(self):
    """
    :return: 模板文件路径
    """
    tempaltes = os.path.join(self.base_dir, 'templates')
    return tempaltes

  def __staticPath__(self):
    """
    :return: 静态文件路径
    """
    static = os.path.join(self.base_dir, 'statics')
    return static

  def useSsl(self):
    """
    :return: 返回ssl配置
    """
    ssl_options = {}
    ca = self.globalConfig.get('ssl')
    if options.ssl:
      ssl_options['certfile'] = ca.get('pubilc')
      ssl_options['keyfile'] = ca.get('private')
    return ssl_options

  def tornadoApp(self):
    """
    :return: 返回生成的APP对象
    """
    totle_route = route.AppRoute().route()
    app_setting = {
      'handlers': totle_route,
      'template_path': self.__tempaltesPath__(),
      'static_path': self.__staticPath__(),
      'login_url': '/login',
      'debug': False,
      'autoreload': False,
      'serve_traceback': True,
      'compiled_template_cache': False,
      'xsrf_cookies': False,
      'cookie_secret': "bQd3T8WSORUGqEdnC6gUtuCp0jUYAm0OIrWJbjHe/zPA':"
    }
    app = tornado.web.Application(**app_setting)
    return app
