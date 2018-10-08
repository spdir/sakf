# -*- coding: utf-8 -*-
# HOME Handler

import tornado.web
from sakf.app.sakf import base


class IndexHandler(base.BaseHandlers):

  @tornado.web.authenticated
  @base.auth_url
  def get(self):
    return self.render('sakf/index.html', username=self.session['username'])

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


class TestHandler(base.BaseHandlers):
  def get(self, *args, **kwargs):
    self.render('sakf/test.html')
