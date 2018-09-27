#-*- coding: utf-8 -*-
import hashlib

def md5_string(string):
  """
  对字符串进行MD5加密
  :param string: 要进行加密的字符串
  :return: 加密后是十六进制字符串
  """
  obj = hashlib.md5()
  obj.update(string.encode('utf-8'))
  encry_string = obj.hexdigest()
  return encry_string