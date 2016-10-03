# coding=utf-8
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    nickname = Column(String(50), nullable=False, default='Новенький')


class Chats(Base):
    __tablename__ = 'chats'

    id = Column(Integer(), primary_key=True)
    chat_name = Column(String(50), nullable=True,)
    chat_type = Column(String(10), nullable=False, default='single')


class ChatRooms(Base):
    __tablename__ = 'chat_rooms'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    chat_id = Column(Integer(), ForeignKey('chats.id'))
    user = relationship(Users)
    chat = relationship(Chats)


class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer(), primary_key=True)
    message = Column(Text(), nullable=False)
    date = Column(DateTime(), nullable=False, default=datetime.now())
    sender_id = Column(Integer(), ForeignKey('users.id'))
    user = relationship(Users)
    chat_id = Column(Integer(), ForeignKey('chats.id'))
    chat = relationship(Chats)


class DeliverMessage(Base):
    __tablename__ = 'deliver_messages'

    id = Column(Integer(), primary_key=True)
    deliver = Column(Boolean(), nullable=False, default=False)
    user_id = Column(Integer(), ForeignKey('users.id'))
    message_id = Column(Integer(), ForeignKey('messages.id'))
