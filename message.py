# coding=utf-8
import time
from datetime import datetime

from db import models_function


class BaseMessage:
    deliver = {}

    def __init__(self, room_id, users):
        """
        Заполняем не доставленными сообщениями если для данной комнаты они есть
        :param room_id:
        """
        self.messages = {}
        self.room_id = room_id

        messages = models_function.get_undelivered_message(room_id, users)

        if messages:
            for message in messages:
                self.messages.update({message.id: self.gen_message(user_id=message.id,
                                                                   message=message.message,
                                                                   file=message.file)})
                users = [user[0] for user in models_function.get_undelivered_users(message.id)]
                self.deliver.update({message.id: users})
        print(self.deliver)

    def add_message(self, user_id, message, chat_id, file):
        """
            Добавление нового сообщения
        :param file:
        :param user_id: id клиента
        :param message: тело сообщения
        """
        new_message = self.gen_message(user_id=user_id, message=message, file=file)

        db_message = models_function.add_message(chat_id=chat_id, user_id=user_id,
                                                 message=message, file=file)
        self.messages.update({db_message.id: new_message})
        return db_message.id

    def change_status(self, message_id, status, user):
        if status:
            models_function.change_message_status(message_id, user_id=user)

            try:
                self.deliver[message_id].remove(user)
            except (ValueError, KeyError):
                pass

            try:
                if not self.deliver[message_id]:
                    self.messages.pop(message_id)
            except KeyError:
                pass
        else:
            models_function.set_message_undelivered(user=user, message_id=message_id, status=status)

            if message_id in self.deliver.keys():
                self.deliver[message_id].append(user)
            else:
                self.deliver[message_id] = [user]

    def get_message(self):
        return self.messages

    def gen_message(self, user_id, message, file):
        return {
            'ts': time.mktime(datetime.now().timetuple()),
            'message': message,
            'sender': user_id,
            'chat_id': self.room_id,
            'file': file
        }
