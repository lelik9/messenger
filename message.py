# coding=utf-8
import time
import models_function

from datetime import datetime


class BaseMessage:
    messages = {}
    deliver = {}

    def __init__(self, room_id, users):
        """
        Заполняем не доставленными сообщениями если для данной комнаты они есть
        :param room_id:
        """
        messages = models_function.get_undelivered_message(room_id, users)
        print(messages)
        if messages:
            for message in messages:
                self.messages.update({message.id:
                    {
                        'ts': time.mktime(message.date.timetuple()),
                        'message': message.message,
                        'sender': message.sender_id,
                        'chat_id': room_id,
                    }})
                users = [user[0] for user in models_function.get_undelivered_users(message.id)]
                self.deliver.update({message.id: users})

        print(self.messages, self.deliver)

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
        }

        db_message = models_function.add_message(chat_id=chat_id, user_id=user_id,
                                                 message=message)
        self.messages.update({db_message.id: new_message})
        return db_message.id

    def change_status(self, message_id, status, user):
        if status:
            models_function.change_message_status(message_id, user_id=user)
            try:
                self.deliver[int(message_id)].remove(int(user))
            except ValueError:
                pass
            if not self.deliver[int(message_id)]:
                self.messages.pop(int(message_id))
        else:
            models_function.set_message_undelivered(user=user, message_id=message_id, status=status)

    def get_message(self):
        return self.messages
