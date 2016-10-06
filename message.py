# coding=utf-8
import time
import models_function

from datetime import datetime


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

                self.messages.update({message.id:
                    {
                        'ts': time.mktime(message.date.timetuple()),
                        'message': message.message,
                        'sender': message.user.nickname,
                        'chat_id': self.room_id,
                    }})
                users = [user[0] for user in models_function.get_undelivered_users(message.id)]
                self.deliver.update({message.id: users})

    def add_message(self, user_id, message, chat_id):
        """
            Добавление нового сообщения
        :param user_id: id клиента
        :param message: тело сообщения
        """
        new_message = {
            'ts': time.mktime(datetime.now().timetuple()),
            'message': message,
            'sender': user_id,
            'chat_id': self.room_id,
        }

        db_message = models_function.add_message(chat_id=chat_id, user_id=user_id,
                                                 message=message)
        self.messages.update({db_message.id: new_message})
        return db_message.id

    def change_status(self, message_id, status, user):
        if status:
            models_function.change_message_status(message_id, user_id=user)
            try:
                self.deliver[message_id].remove(user)
            except ValueError:
                pass
            if not self.deliver[message_id]:
                self.messages.pop(message_id)
        else:
            models_function.set_message_undelivered(user=user, message_id=message_id, status=status)

            if message_id in self.deliver.keys():
                self.deliver[message_id].append(user)
            else:
                self.deliver[message_id] = [user]

    def get_message(self):
        return self.messages
