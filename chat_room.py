# coding=utf-8
from tornado.concurrent import Future

from db import models_function
from message import BaseMessage


def send_waiter(users, user_id, result):
    for user in users:
        if user != int(user_id):
            waiting = rooms.get_waiting(str(user))
            if waiting is not None:
                waiting.set_result(result)


class Room:
    status = ''

    def __init__(self, *, users, room_id, room_type='private'):
        self.id = room_id
        self.users = users
        self.room_type = room_type
        self._messages = BaseMessage(self.id, self.users)

    def add_message(self, message, user_id, file):
        message_id = self._messages.add_message(message=message, user_id=user_id, chat_id=self.id,
                                                file=file)

        for user in self.users:
            if user != int(user_id):
                self._messages.change_status(message_id=message_id, user=user, status=False)
                waiting = rooms.get_waiting(str(user))

                if waiting is not None:
                    waiting.set_result({'type': 'message', 'messages': self._messages.get_message()})

    def change_message_status(self, user, message_id):
        self._messages.change_status(message_id=message_id, user=user, status=True)

    def change_user_status(self, user_id):
        send_waiter(users=self.users, user_id=user_id, result={'type': 'status', 'typing': 1})


class Users:
    users_status = {}

    def __init__(self):
        self.generate_list()

    def generate_list(self):
        for user in models_function.get_users_list():
            self.users_status.update({
                user[0]: {
                    'nick': user[1],
                    'status': 0
                }
            })

    def change_status(self, user_id, status):
        user_id = int(user_id)
        if user_id in self.users_status.keys():

            self.users_status[user_id]['status'] = status
        else:
            self.generate_list()
            self.users_status[user_id]['status'] = status

        send_waiter(users=self.users_status.keys(), user_id=user_id, result={'type': 'status', 'online': status})

    def get_users(self):
        return self.users_status


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
        self._users = Users()

    def get_users(self):
        return self._users.get_users()

    def register_room(self, room_model):
        if room_model:
            room_id = room_model.id
            room_type = room_model.chat_type
            users = [user[0] for user in models_function.get_room_users(room_id)]

            new_room = Room(users=users, room_id=room_id, room_type=room_type)
            self.all_rooms.update({room_id: new_room})
            return new_room

    def get_room(self, room_id):
        if room_id in self.all_rooms.keys():
            room = self.all_rooms.get(room_id)
        else:
            room = models_function.get_room(room_id)
            room = self.register_room(room)
        return room

    @staticmethod
    def create_group_room(users, group_name, group_type):
        chat_id = None

        if group_type == 'private':
            chat_id = models_function.find_users_room(users=users)

        if chat_id is None:
            chat_id = models_function.create_chat_room(group_name, group_type).id
            models_function.add_chat_room(chat_id, users)

        return chat_id

    def add_waiting(self, id):
        """
            Создание "ожидающего"
        :param id: id "ожидающего"
        :return:
        """
        waiting = Future()
        self.pending.update({id: waiting})
        self._users.change_status(id, 1)
        print('waiting: {}'.format(self.pending))
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
        self._users.change_status(id, 0)

    def get_waiting(self, wait_id):
        if wait_id in self.pending.keys():
            return self.pending.pop(wait_id)


rooms = Rooms()
