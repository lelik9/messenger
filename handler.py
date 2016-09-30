# coding=utf-8
import time
import tornado.web

import models_function

from chat_room import rooms
from tornado import gen


def write(*, req, msg_type, msg):
    req.write({
        'type': msg_type,
        'result': msg,
    })


class MessageNewHandler(tornado.web.RequestHandler):
    def post(self):
        my_id = self.get_argument('my_id')
        user_id = self.get_argument('user_id')
        message = self.get_argument('message')

        room = rooms.get_user_room(my_id, user_id)
        room.add_message(user_id=my_id, message=message, chat_id=room.id)

    def get(self, *args, **kwargs):
        users = self.get_argument('users').split(',')
        message = self.get_argument('message')
        chat_id = self.get_argument('chat_id')

        if chat_id != '0':
            room = rooms.get_group_room(chat_id)
        else:
            room = rooms.get_user_room(users)

        if room:
            room.add_message(user_id=users[0], message=message, chat_id=room.id)
        else:
            self.write(dict(error='Chat not found'))


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
            write(req=self, msg_type='message', msg=msg)
        else:
            waiting = rooms.add_waiting(my_id)
            message = yield waiting

            write(req=self, msg_type='message', msg=message)


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

        write(req=self, msg_type='users', msg=users)


class MessageRangeHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        users = self.get_argument('users').split(',')
        range = int(self.get_argument('range'))
        last_message = int(self.get_argument('last_message'))

        messages = models_function.get_last_messages(users=users, range=range, last=last_message)

        msg = {}

        for message in messages:
            msg.update({message.id: {
                'ts': time.mktime(message.date.timetuple()),
                'message': message.message,
                'sender': message.sender_id,
                'deliver': message.deliver
            }})

        write(req=self, msg_type='message', msg=msg)


class GroupHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        """
        Create group chat
        :param args:
        :param kwargs:
        :return:
        """

        my_id = self.get_argument('my_id')
        group_name = self.get_argument('group_name')