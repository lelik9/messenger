# coding=utf-8
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    nickname = Column(String(50), nullable=False, default='Новенький')
    active = Column(Boolean(), nullable=False, default=True)


class UsersAuth(Base):
    __tablename__ = 'users_auth'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    uuid = Column(String(100), nullable=False, )
    token = Column(String(100), nullable=False)
    user = relationship(Users, backref=backref('users', cascade="all, delete"))


class Chats(Base):
    __tablename__ = 'chats'

    id = Column(Integer(), primary_key=True)
    chat_name = Column(String(50), nullable=True, )
    chat_type = Column(String(10), nullable=False, default='single')
    active = Column(Boolean(), nullable=False, default=True)


class ChatRooms(Base):
    __tablename__ = 'chat_rooms'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    chat_id = Column(Integer(), ForeignKey('chats.id'))
    user = relationship(Users, cascade="all, delete")
    chat = relationship(Chats, backref=backref('chats', cascade="all, delete"))


class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer(), primary_key=True)
    message = Column(Text(), nullable=False)
    date = Column(DateTime(), nullable=False, default=datetime.now())
    file = Column(Text(), nullable=False, default='0')
    sender_id = Column(Integer(), ForeignKey('users.id'))
    user = relationship(Users, cascade="all, delete")
    chat_id = Column(Integer(), ForeignKey('chats.id'))
    chat = relationship(Chats, )


class DeliverMessage(Base):
    __tablename__ = 'deliver_messages'

    id = Column(Integer(), primary_key=True)
    deliver = Column(Boolean(), nullable=False, default=False)
    user_id = Column(Integer(), ForeignKey('users.id'))
    user = relationship(Users, cascade="all, delete")
    message_id = Column(Integer(), ForeignKey('messages.id'))
    message = relationship(Messages, cascade="all, delete")


class Files(Base):
    __tablename__ = 'files'

    id = Column(Text(), primary_key=True)
    name = Column(String(10), nullable=False)
