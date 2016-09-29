# coding=utf-8
import tornado.ioloop
import tornado.httpserver

from tornado.options import define, options, parse_command_line
from urls import url


if __name__ == '__main__':
    app = url()
    define("port", default=8887, help="run on the given port", type=int)
    parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

