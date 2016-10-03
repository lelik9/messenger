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

    # def get_user_room(self, users):
    #     room = models_function.get_room_id(users)
    #     print(room.id)
    #
    #     if not room:
    #         room = self.create_user_room(users)
    #
    #     if room.id not in self.all_rooms.keys():
    #         room = self.register_user_room(room.id, users)
    #     else:
    #         room = self.all_rooms.get(room.id)
    #
    #     return room
    #
    def register_room(self, room_model):
        room_id = room_model.id
        room_type = room_model.chat_type
        users = [user[0] for user in models_function.get_room_users(room_id)]

        new_room = Room(users=users, room_id=room_id, room_type=room_type)
        self.all_rooms.update({room_id: new_room})
        return new_room
    #
    # def register_user_room(self, room_id, users):
    #     new_room = Room(users=users, room_id=room_id)
    #     new_room.id = room_id
    #     self.all_rooms.update({room_id: new_room})
    #
    #     return new_room
    #
    # @staticmethod
    # def create_user_room(users):
    #     chat = models_function.create_chat_room('', 'single')
    #     models_function.add_chat_room(chat.id, users)
    #     return chat

    def get_room(self, room_id):
        if room_id in self.all_rooms.keys():
            room = self.all_rooms.get(room_id)
        else:
            room = models_function.get_room(room_id)
            room = self.register_room(room)
        return room

    @staticmethod
    def create_group_room(users, group_name, group_type):
        chat = models_function.create_chat_room(group_name, group_type)
        models_function.add_chat_room(chat.id, users)

        return chat.id

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

    def __init__(self, *, users, room_id, room_type='private'):
        self.id = room_id
        self.users = users
        self.room_type = room_type
        self._messages = BaseMessage(self.id, self.users)

    def add_message(self, message, user_id, chat_id):
        message_id = self._messages.add_message(message=message, user_id=user_id, chat_id=chat_id)
        # self._messages.set_message_undelivered(users=self.users, message_id=message_id)

        for user in self.users:
            if user != int(user_id):
                self._messages.change_status(message_id=message_id, user=user, status=False)
                waiting = rooms.get_waiting(str(user))
                if waiting is not None:
                    waiting.set_result(self._messages.get_message())


rooms = Rooms()
