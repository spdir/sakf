# -*- coding: utf-8 -*-
# Url
from sakf.app.sakf import base


class UrlHandler(base.BaseHandlers):

  def get(self, suburl, *args, **kwargs):
    return self.render('auth/urls.html')

  def post(self, suburl, *args, **kwargs):
    self.get()
