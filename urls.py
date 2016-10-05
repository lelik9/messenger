# coding=utf-8
import tornado.web

from handler import MessageHandler, MessageDeliverHandler, \
    UsersListHandler, MessageRangeHandler, ChatHandler


def url():
    app = tornado.web.Application(
        [
            # (r"/", MainHandler),
            (r"/message/", MessageHandler),
            (r"/message/", MessageHandler),
            (r"/message/delivery/", MessageDeliverHandler),
            (r"/message/range/", MessageRangeHandler),
            (r'/group/', ChatHandler),
            (r"/users/", UsersListHandler),
        ],
    )
    return app
