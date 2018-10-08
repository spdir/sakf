# -*- coding: utf-8 -*-
from sakf.app.sakf import base


class Test1Handler(base.BaseHandlers):
  def get(self, *args, **kwargs):
    return self.write('get')

  def post(self, *args, **kwargs):
    a = self.get_argument('tp', None)
    print(a)
    return self.write('post')


