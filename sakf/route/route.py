# -*- coding: utf-8 -*-
# app route
from tornado.options import options
from sakf.conf import serverConfig
# ------------- start handler -------------#
from sakf.app.sakf import home, test
from sakf.app.auth import (auth, user, group, url)


# ------------- end handler -------------#


class AppRoute(object):
  """
  声明APP路由
  """

  @classmethod
  def __sakf__(self):
    """
    main app route
    :return: list
    """
    sakf_route = [
      (r'/', home.IndexHandler),
      (r'/home', home.HomeHandler),
      (r'/setting/?', home.HomeSettingHandler),
      (r'/test/?', home.TestHandler),
      (r'/test1/?', test.Test1Handler),
    ]
    return sakf_route

  @classmethod
  def __auth__(self):
    auth_route = [
      (r'/login/?', auth.LoginHandler),
      (r'/logout/?', auth.LogoutHandler),
      (r'/auth/group/?(?P<suburl>.*)', group.GroupHandler),
      (r'/auth/user/?(?P<suburl>.*)', user.UserHandler),
      (r'/auth/url/?(?P<suburl>.*)', url.UrlHandler)
    ]
    return auth_route

  def route(self):
    """
    返回所有app路由
    :return: list
    """
    app_route = []
    app_container = (
      self.__sakf__(),
      self.__auth__()
    )
    for app in app_container:
      if len(app[0]) == 0:
        continue
      app_route.extend(app)
    return app_route
