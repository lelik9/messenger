# coding=utf-8
import ssl

import tornado.httpserver
from tornado.options import define, options, parse_command_line

from db import init_db

if __name__ == '__main__':
    init_db.init_db()

    from urls import url

    app = url()
    define("port", default=8887, help="run on the given port", type=int)
    parse_command_line()

    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain("cert/mydomain.crt", "cert/mydomain.key")

    http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_ctx)
    http_server.listen(options.port)
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print("")