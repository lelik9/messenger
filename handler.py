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
        user = self.get_argument('user')
        message = self.get_argument('message')
        chat_id = self.get_argument('chat_id')

        room = rooms.get_room(chat_id)

        if room:
            room.add_message(user_id=user, message=message)
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
        print(messages)
        if messages:
            msg = {}

            for message in messages:
                msg.update({message.id: {
                    'ts': time.mktime(message.date.timetuple()),
                    'message': message.message,
                    'sender': message.user.nickname,
                }})
            write(req=self, msg_type='message', msg=msg)
        else:
            waiting = rooms.add_waiting(my_id)
            message = yield waiting

            write(req=self, msg_type='message', msg=message)


class MessageDeliverHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        message_id = int(self.get_argument('message_id'))
        status = self.get_argument('status')
        user = int(self.get_argument('user'))
        chat_id = self.get_argument('chat_id')

        room = rooms.get_room(chat_id)

        if room:
            room.change_message_status(user=user, message_id=message_id, status=status)


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


class ChatHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        """
        Get users chat rooms.
        :param args:
        :param kwargs:
        :return:
        """

        # STUB!
        users = self.get_argument('users').split(',')
        group_name = self.get_argument('group_name')
        group_type = self.get_argument('group_type')

        room_id = rooms.create_group_room(users=users, group_name=group_name, group_type=group_type)

        write(req=self, msg_type='group', msg={'room_id': room_id})

    def post(self, *args, **kwargs):
        """
        Create new chat room (private or group)
        :param args:
        :param kwargs:
        :return:
        """

        users = self.get_argument('users').split(',')
        group_name = self.get_argument('group_name')
        group_type = self.get_argument('group_type')

        room_id = rooms.create_group_room(users=users, group_name=group_name, group_type=group_type)

        write(req=self, msg_type='group', msg={'room_id': room_id})
