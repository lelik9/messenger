# coding=utf-8
import tornado.web

from handler import MessageHandler, MessageDeliverHandler, \
    UsersListHandler, MessageRangeHandler, ChatHandler, ChangeChatHandler

from user_auth_handler import UserHandler, LoginHandler, DeleteUserHandler


def url():
    app = tornado.web.Application(
        [
            (r"/", UserHandler),
            (r'/login', LoginHandler),
            (r"/message/", MessageHandler),
            (r"/message/", MessageHandler),
            (r"/message/delivery/", MessageDeliverHandler),
            (r"/message/range/", MessageRangeHandler),
            (r'/group/', ChatHandler),
            (r'/group/change/', ChangeChatHandler),
            (r"/users/", UsersListHandler),
            (r"/users/delete/", DeleteUserHandler),
        ],
        autoreload=True,
        cookie_secret="156783452358345379456676458767",
        login_url="/login",
    )
    return app
