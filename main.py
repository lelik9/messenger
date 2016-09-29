# coding=utf-8
from db_func import db
import models
import models_function
import tornado.escape
import tornado.ioloop
import tornado.httpserver

from tornado.options import define, options, parse_command_line
from urls import url


def fill_users():
    for i in range(10):
        models_function.add_user('User'+str(i))

if __name__ == '__main__':
    # db.generate_db(models.Base)
    # fill_users()

    app = url()
    define("port", default=8887, help="run on the given port", type=int)
    parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

