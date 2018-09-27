# -*- coding: utf-8 -*-
# User
from sakf.app.sakf import base


class UserHandler(base.BaseHandlers):

  def get(self, suburl, *args, **kwargs):
    return self.write('user')

  def post(self, suburl, *args, **kwargs):
    self.get()
