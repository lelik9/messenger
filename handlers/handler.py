# coding=utf-8
import common

import json
import time
import tornado.web

from chat_room import rooms
from db import models_function

from os import makedirs
from os.path import exists
from tornado import gen


def write(*, req, msg_type, msg):
    req.write({
        'type': msg_type,
        'result': msg,
    })
    req.flush()


def gen_messages(messages):
    msg = {}

    for message in messages:
        msg.update({message.id: {
            'ts': time.mktime(message.date.timetuple()),
            'message': message.message,
            'sender': message.sender_id,
            'chat_id': message.chat_id,
            'file': message.file,
        }})

    return msg


def add_message(req, user, chat_id, message, file):
    room = rooms.get_room(chat_id)

    if room:
        room.add_message(user_id=user, message=message, file=file)
        write(req=req, msg_type='success', msg={'status': 'send'})
    else:
        write(req=req, msg_type='error', msg='Chat not found')


class BaseHandler(tornado.web.RequestHandler):
    def prepare(self):
        try:
            auth = self.request.headers.get('Authorization').split('=')
            user = auth[0]
            token = auth[1]

            # if not models_function.check_user_token(user_id=user, token=token):
            #     self.send_error(401)
        except AttributeError:
            pass
            # self.send_error(401)


class MessageHandler(BaseHandler):
    def post(self):
        user = self.get_argument('user')
        message = self.get_argument('message')
        chat_id = self.get_argument('chat_id')

        add_message(req=self, user=user, chat_id=chat_id, message=message, file='0')

    @gen.coroutine
    def get(self, *args, **kwargs):
        user = self.get_argument('user')
        messages = models_function.get_user_undelivered_message(user)

        if messages:
            message = {'type': 'message', 'messages': gen_messages(messages)}
        else:
            waiting = rooms.add_waiting(user)
            message = yield waiting

        write(req=self, msg_type='success', msg=message)


class MessageDeliverHandler(BaseHandler):
    def post(self, *args, **kwargs):
        messages = json.loads(self.get_argument('messages'))
        user = int(self.get_argument('user'))

        for k, v in messages.items():
            room = rooms.get_room(v['chat_id'])

            if room:
                room.change_message_status(user=user, message_id=int(k))


class UsersListHandler(BaseHandler):
    def get(self, *args, **kwargs):
        users = rooms.get_users()

        write(req=self, msg_type='success', msg=users)


class MessageRangeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        msg_range = int(self.get_argument('range'))
        last_message = int(self.get_argument('last_message'))
        chat_id = int(self.get_argument('chat_id'))

        messages = models_function.get_last_messages(msg_range=msg_range,
                                                     last=last_message, chat_id=chat_id)

        msg = gen_messages(messages)

        write(req=self, msg_type='message', msg=msg)


class ChatHandler(BaseHandler):
    def get(self, *args, **kwargs):
        """
        Get users chat rooms.
        :param args:
        :param kwargs:
        :return:
        """

        user = self.get_argument('user')

        res = models_function.get_rooms_list(user)
        write(req=self, msg_type='success', msg=res)

    def post(self, *args, **kwargs):
        """
        Create new chat room (private or group)
        :param args:
        :param kwargs:
        :return:
        """
        # print(args, kwargs, self.get_query_argument('group_name'))
        users = self.get_argument('users').split(',')
        group_name = self.get_argument('group_name')
        group_type = self.get_argument('group_type')

        room_id = rooms.create_group_room(users=users, group_name=group_name, group_type=group_type)

        write(req=self, msg_type='success', msg={'chat_id': room_id, 'chat_name': group_name})


class ChangeChatHandler(BaseHandler):
    def get(self, *args, **kwargs):
        """
        Rename chat. Only for group chat
        :param args:
        :param kwargs:
        :return:
        """
        chat_name = self.get_argument('chat_name')
        chat_id = self.get_argument('chat_id')

        result = models_function.rename_chat(chat_id=chat_id, chat_name=chat_name)

        if result:
            write(req=self, msg_type='success', msg='ok')
        else:
            write(req=self, msg_type='error', msg='Chat rename failed')

    def post(self, *args, **kwargs):
        """
        Delete chat
        :param args:
        :param kwargs:
        :return:
        """
        chat_id = self.get_argument('chat_id')

        result = models_function.mark_delete_chat(chat_id=chat_id)

        if not result:
            write(req=self, msg_type='error', msg='Chat remove failed')
        else:
            write(req=self, msg_type='success', msg='Chat remove OK')


class ChatUserChangeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        """
        Ivite user to group chat
        :param args:
        :param kwargs:
        :return:
        """
        chat_id = self.get_argument('chat_id')
        user = self.get_argument('user')

        result = models_function.invite_user(user_id=user, chat_id=chat_id)

        if not result:
            write(req=self, msg_type='error', msg='Invite user failed')
        else:
            write(req=self, msg_type='success', msg='User invited')

    def post(self, *args, **kwargs):
        chat_id = self.get_argument('chat_id')
        user = self.get_argument('user')

        result = models_function.remove_user_from_chat(user_id=user, chat_id=chat_id)

        if not result:
            write(req=self, msg_type='error', msg='Remove user from chat failed')
        else:
            write(req=self, msg_type='success', msg='User deleted from chat')


class FileHadler(BaseHandler):
    def post(self, *args, **kwargs):
        user = int(self.get_argument('user'))
        chat_id = self.get_argument('chat_id')
        file_name = self.get_argument('file_name')

        new_file = models_function.add_file(file_name)
        uuid = new_file.id

        if not exists(common.DATA_PATH):
            makedirs(common.DATA_PATH)

        with open(common.DATA_PATH + '/' + uuid, 'wb') as f:
            res = self.request.body
            f.write(res)

        add_message(req=self, user=user, chat_id=chat_id, message=file_name, file=uuid)

    def get(self, *args, **kwargs):
        file_id = self.get_argument('file_id')

        with open(common.DATA_PATH + '/' + file_id, 'rb') as f:
            self.write(f.read())


class ChangeUserStatus(BaseHandler):
    def get(self, *args, **kwargs):
        user = int(self.get_argument('user'))
        chat_id = self.get_argument('chat_id')

        room = rooms.get_room(chat_id)
        room.change_user_status(user_id=user)
