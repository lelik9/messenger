# coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DB(object):

    def __init__(self):
        self.engine = self._make_connection()
        self.session = self._get_session(self.engine)

    def _make_connection(self):
        return create_engine('sqlite:///sql.db')

    def _get_session(self, engine):
        DBSession = sessionmaker(bind=engine)
        return DBSession()

    def generate_db(self, base):
        base.metadata.create_all(self.engine)

    def add(self, transaction):
        self.session.add(transaction)
        self.session.commit()


db = DB()
