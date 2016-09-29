# coding=utf-8
import tornado.web

from handler import MessageNewHandler, MessageUpdatesHandler, MessageDeliverHandler, \
    UsersListHandler, MessageRangeHandler, GroupHandler


def url():
    app = tornado.web.Application(
        [
            # (r"/", MainHandler),
            (r"/message/new/", MessageNewHandler),
            (r"/message/updates/", MessageUpdatesHandler),
            (r"/message/delivery/", MessageDeliverHandler),
            (r"/message/range/", MessageRangeHandler),
            (r'/group/', GroupHandler),
            (r"/users/", UsersListHandler),
        ],
    )
    return app
