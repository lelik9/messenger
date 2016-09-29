# coding=utf-8
import time
import tornado.web

import models_function

from chat_room import rooms
from tornado import gen


class MessageNewHandler(tornado.web.RequestHandler):
    def post(self):
        pass

    def get(self, *args, **kwargs):
        my_id = self.get_argument('my_id')
        user_id = self.get_argument('user_id')
        message = self.get_argument('message')

        room = rooms.get_user_room(my_id, user_id)
        room.add_message(user_id=my_id, message=message, chat_id=room.id)


class MessageUpdatesHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        pass

    @gen.coroutine
    def get(self, *args, **kwargs):
        my_id = self.get_argument('my_id')
        messages = models_function.get_user_undelivered_message(my_id)

        if messages:
            msg = {}

            for message in messages:
                msg.update({message.id: {
                    'ts': time.mktime(message.date.timetuple()),
                    'message': message.message,
                    'sender': message.sender_id,
                    'deliver': message.deliver
                }})
            self.write(dict(messages=msg))
        else:
            waiting = rooms.add_waiting(my_id)
            message = yield waiting

            self.write(dict(messages=message))


class MessageDeliverHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        message_id = self.get_argument('message_id')
        status = self.get_argument('status')

        if status == 'true':
            models_function.change_message_status(message_id)


class UsersListHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        my_id = self.get_argument('my_id')

        users = models_function.get_users_list(my_id)
        # users = [user.__dict__ for user in users]
        print(users)
        self.write(dict(users=users))


class MessageRangeHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        res = models_function.get_last_messages(1, 2, 5, 4)

        for r in res:
            print(r.id)
