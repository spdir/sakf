# -*- coding: utf-8 -*-
import logging
import tornado.ioloop
from tornado.httpserver import HTTPServer
from tornado.options import options, parse_command_line
from sakf.conf import serverConfig

ioloop = tornado.ioloop.IOLoop.current()


def main():
  parse_command_line()
  app_obj = serverConfig.ServerApp()
  app = app_obj.tornadoApp()
  if options.ssl:
    ssl_conf = app_obj.useSsl()
    httpserver = HTTPServer(app, ssl_options=ssl_conf)
  else:
    httpserver = HTTPServer(app)
  httpserver.bind(address=options.address, port=options.port)
  httpserver.start()
  _is_ssl = '(ssl)'
  if not options.ssl:
    _is_ssl = ''
  fb = {
    'ssl': _is_ssl,
    'addr': options.address,
    'port': options.port
  }
  logging.info("\033[32mListening start{ssl} -> {addr}:{port}\033[0m".format(**fb))
  ioloop.start()
