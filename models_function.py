# coding=utf-8
from sqlalchemy.orm import exc
from sqlalchemy.orm import aliased
from datetime import datetime

from db_func import db
from models import Messages, Users, Chats, ChatRooms, DeliverMessage


def add_message(*, message, user_id, chat_id):
    print(message, user_id, chat_id)
    new_message = Messages(message=message,
                           date=datetime.now(),
                           sender_id=user_id,
                           chat_id=chat_id)
    db.add(new_message)
    return new_message


def set_message_undelivered(user, message_id, status):
    deliver = DeliverMessage(user_id=user, message_id=message_id, deliver=status)
    db.add(deliver)


def get_undelivered_message(chat_id, users):
    return db.session.query(Messages).filter(Messages.chat_id == chat_id,
                                             ChatRooms.chat_id == chat_id,
                                             DeliverMessage.deliver == 0,
                                             DeliverMessage.user_id.in_(users)).all()


def get_rooms_with_undelivered_message():
    return db.session.query(Chats).filter(Chats.id == Messages.chat_id,
                                          Messages.id == DeliverMessage.message_id,
                                          DeliverMessage.deliver == 0).all()


def add_user(nick):
    new_user = Users(nickname=nick)
    db.add(new_user)


def create_chat_room(name, chat_type):
    new_chat = Chats(chat_name=name, chat_type=chat_type)
    db.add(new_chat)
    return new_chat


def add_chat_room(chat_id, users):
    for user in users:
        db.add(ChatRooms(chat_id=chat_id, user_id=user))


def get_room(room_id):
    try:
        return db.session.query(Chats).filter(Chats.id == room_id).one()
    except exc.NoResultFound:
        return False


def get_room_users(chat_id):
    return db.session.query(ChatRooms.user_id).filter(ChatRooms.chat_id == chat_id).all()


def get_user_undelivered_message(user_id):
    return db.session.query(Messages).filter(ChatRooms.user_id == user_id,
                                             Messages.chat_id == ChatRooms.chat_id,
                                             Messages.sender_id != user_id,
                                             DeliverMessage.user_id == user_id,
                                             DeliverMessage.deliver == 0).all()


def change_message_status(message_id, user_id):
    try:
        message = db.session.query(DeliverMessage).filter(DeliverMessage.message_id == message_id,
                                                          DeliverMessage.user_id == user_id).one()
        message.deliver = True
        db.session.dirty
        db.session.commit()
    except exc.NoResultFound:
        return False


def get_users_list(user_id):
    return db.session.query(Users.id, Users.nickname).filter(Users.id != user_id).all()


def get_last_messages(*, msg_range, last, chat_id):
    query = db.session.query(Messages).filter(Messages.chat_id == chat_id)

    if last != 0:
        query = query.filter(Messages.id < last)

    query = query.order_by(Messages.id.desc()).limit(msg_range)

    return query.all()


def get_undelivered_users(message_id):
    return db.session.query(DeliverMessage.user_id).filter(DeliverMessage.message_id == message_id,
                                                           DeliverMessage.deliver == 0).all()


def find_users_room(users):
    tbl1 = aliased(ChatRooms)
    tbl2 = aliased(ChatRooms)
    try:
        res = db.session.query(tbl1.chat_id).filter(tbl1.user_id == users[0],
                                                    tbl2.user_id == users[1],
                                                    tbl1.chat_id == tbl2.chat_id).one()
        return res[0]
    except exc.NoResultFound:
        return None


def get_rooms_list(user):
    tbl1 = aliased(ChatRooms)
    tbl2 = aliased(ChatRooms)
    query = db.session.query(tbl2.chat_id, Chats.chat_name, Chats.chat_type, Users.nickname)
    query = query.join(Chats).join(Users).filter(tbl1.user_id == user,
                                                 tbl2.user_id != user,
                                                 tbl1.chat_id == tbl2.chat_id).group_by(
        tbl1.chat_id).all()
    return query


def rename_chat(chat_id, chat_name):
    try:
        chat = db.session.query(Chats).filter(Chats.id == chat_id).one()
        chat.name = chat_name
        db.session.dirty
        db.session.commit()
    except exc.NoResultFound:
        return False
