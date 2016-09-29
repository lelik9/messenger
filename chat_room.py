# coding=utf-8
import functools
import models_function
import random

from collections import namedtuple
from tornado.concurrent import Future

from message import BaseMessage


class Rooms:
    all_rooms = {}
    pending = {}

    def __init__(self):
        """
        Restore rooms from DB
        """
        rooms = models_function.get_rooms_with_undelivered_message()
        print(rooms)
        for room in rooms:
            self.register_room(room)

    def get_user_room(self, users):
        room = models_function.get_room_id(users)

        if not room:
            room = self.create_user_room(users)

        if room.id not in self.all_rooms.keys():
            room = self.register_user_room(room.id, users)
        else:
            room = self.all_rooms.get(room.id)

        return room

    def register_room(self, room_model):
        room_id = room_model.id
        room_type = room_model.chat_type
        users = [model.user_id for model in models_function.get_room_users(room_id)]

        new_room = Room(users=users, room_id=room_id, room_type=room_type)
        self.all_rooms.update({room_id: new_room})

    def register_user_room(self, room_id, users):
        new_room = Room(users=users, room_id=room_id)
        new_room.id = room_id
        self.all_rooms.update({room_id: new_room})

        return new_room

    @staticmethod
    def create_user_room(users):
        chat = models_function.add_room('', 'single')
        models_function.add_chat_room(chat.id, users)
        return chat

    def get_group_room(self, room_id):
        if room_id in self.all_rooms.keys():
            room = self.all_rooms.get(room_id)
        else:
            return
        return room

    def create_group_room(self, users, group_name):
        chat = models_function.add_room(group_name, 'group')
        models_function.add_chat_room(chat.id, users)

        room = Room(users=users, room_id=chat.id, room_type='group')
        self.all_rooms.update({room.id: room})

        return room

    def add_waiting(self, id):
        """
            Создание "ожидающего"
        :param id: id "ожидающего"
        :return:
        """
        waiting = Future()
        self.pending.update({id: waiting})
        return waiting

    def del_waiting(self, id):
        """
            Удаление "ожидающего"
        :param id: id "ожидающего"
        :return:
        """
        waiting = self.pending.pop(id)
        # Set an empty result to unblock any coroutines waiting.
        waiting.set_result([])

    def get_waiting(self, wait_id):
        if wait_id in self.pending.keys():
            return self.pending.pop(wait_id)


class Room:

    def __init__(self, *, users, room_id, room_type='single'):
        self.id = room_id
        self.users = users
        self.room_type = room_type
        self._messages = BaseMessage(self.id)

    def add_message(self, message, user_id, chat_id):
        self._messages.add_message(message=message, user_id=user_id, chat_id=chat_id)

        for user in self.users:
            if user != int(user_id):
                waiting = rooms.get_waiting(str(user))
                if waiting is not None:
                    waiting.set_result(self._messages.get_message(1))


rooms = Rooms()
