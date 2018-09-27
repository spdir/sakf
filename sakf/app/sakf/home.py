# -*- coding: utf-8 -*-
# HOME Handler

from sakf.app.sakf import base
import tornado.web


class IndexHandler(base.BaseHandlers):

  @tornado.web.authenticated
  @base.auth_url
  def get(self):
    return self.render('sakf/index.html')

  def post(self):
    self.get()


class HomeHandler(base.BaseHandlers):

  @tornado.web.authenticated
  @base.auth_url
  def get(self):
    return self.render('sakf/home.html')

  def post(self):
    return self.get()


class HomeSettingHandler(base.BaseHandlers):

  @tornado.web.authenticated
  @base.auth_url
  def get(self, *args, **kwargs):
    return self.render('sakf/setting.html')

  def post(self, *args, **kwargs):
    self.get()
