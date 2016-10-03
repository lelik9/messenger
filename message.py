# coding=utf-8
import time
import models_function

from datetime import datetime


class BaseMessage:
    messages = {}

    """
            self.message = {
            'ts': time.mktime(datetime.now().timetuple()),
            'type': self.type,
            'message': mes
        }
    """

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
                        'deliver': message.deliver,
                        'chat_id': room_id,
                    }})

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
            'deliver': False
        }

        db_message = models_function.add_message(chat_id=chat_id, user_id=user_id,
                                                 message=message)
        self.messages.update({db_message.id: new_message})
        return db_message.id

    # def set_message_undelivered(self, users, message_id):
    #     models_function.set_message_undelivered(user=user, message_id=message_id)

    def change_status(self, message_id, status, user):
        models_function.set_message_undelivered(user=user, message_id=message_id, status=status)
        # if mess_id in self.messages.keys():
        #     self.messages.pop(mess_id)

    def get_message(self):
        return self.messages
