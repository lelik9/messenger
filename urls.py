# coding=utf-8
import tornado.web


from handler import MessageNewHandler, MessageUpdatesHandler, MessageDeliverHandler


def url():
    app = tornado.web.Application(
        [
            # (r"/", MainHandler),
            (r"/message/new/client/", MessageNewHandler),
            (r"/message/updates/client/", MessageUpdatesHandler),
            (r"/message/delivery/", MessageDeliverHandler),
            # (r"/message/new/server/", MessageNewHandlerServer),
            ],
        )
    return app
