# coding=utf-8
import tornado.web
from handlers.user_auth_handler import UserHandler, UserAuthHandler, LoginHandler, DeleteUserHandler

from handlers.handler import MessageHandler, MessageDeliverHandler, \
    UsersListHandler, MessageRangeHandler, ChatHandler, ChangeChatHandler, ChatUserChangeHandler, \
    FileHadler, ChangeUserStatus


def url():
    app = tornado.web.Application(
        [
            (r"/", UserHandler),
            (r'/login', LoginHandler),
            (r"/message/", MessageHandler),
            (r"/status/", ChangeUserStatus),
            (r"/message/delivery/", MessageDeliverHandler),
            (r"/message/range/", MessageRangeHandler),
            (r'/group/', ChatHandler),
            (r'/group/change/', ChangeChatHandler),
            (r'/group/user/', ChatUserChangeHandler),
            (r"/users/", UsersListHandler),
            (r"/users/delete/", DeleteUserHandler),
            (r'/users/auth/', UserAuthHandler),
            (r'/file/', FileHadler),
        ],
        autoreload=True,
        cookie_secret="156783452358345379456676458767",
        login_url="/login",
    )
    return app