# coding=utf-8
from datetime import datetime

from db_func import db
from models import Messages, Users, Chats, ChatRooms


def add_message(*, message, user_id, chat_id):
    print(message, user_id, chat_id)
    new_message = Messages(message=message,
                           date=datetime.now(),
                           sender_id=user_id,
                           chat_id=chat_id)
    db.add(new_message)
    return new_message


def get_undelivered_message(chat_id):
    return db.session.query(Messages).filter(Messages.chat_id == chat_id,
                                             Messages.deliver == 0).all()


def get_rooms_with_undelivered_message():
    return db.session.query(Chats).filter(Chats.id == Messages.chat_id, Messages.deliver == 0).all()


def add_user(nick):
    new_user = Users(nickname=nick)
    db.add(new_user)


def add_room(name, chat_type):
    new_chat = Chats(chat_name=name, chat_type=chat_type)
    db.add(new_chat)
    return new_chat


def add_chat_room(chat_id, user1, user2):
    user1_room = ChatRooms(chat_id=chat_id, user_id=user1)
    user2_room = ChatRooms(chat_id=chat_id, user_id=user2)

    db.add(user1_room)
    db.add(user2_room)


def get_room_id(user1, user2):
    return db.session.query(ChatRooms).filter(ChatRooms.user_id.in_((user1, user2)),
                                              Chats.chat_type == 'single').group_by(
        ChatRooms.chat_id).one()


def get_room_users(chat_id):
    return db.session.query(ChatRooms).filter(ChatRooms.chat_id == chat_id).all()


def get_user_undelivered_message(user_id):
    return db.session.query(Messages).filter(ChatRooms.user_id == user_id, Messages.sender_id !=
                                             user_id, Messages.deliver == 0).all()


def change_message_status(message_id):
    message = db.session.query(Messages).filter(Messages.id == message_id).one()

    if message:
        message.deliver = True
        db.session.dirty
        db.session.commit()
