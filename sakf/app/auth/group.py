# -*- coding: utf-8 -*-
# Group
from sakf.app.sakf import base


class GroupHandler(base.BaseHandlers):

  @base.auth_url
  def get(self, suburl, *args, **kwargs):
    return self.write('group')

  def post(self, suburl, *args, **kwargs):
    self.get()
