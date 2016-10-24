# coding=utf-8

from common import SQLITE_FILE_PATH
from db import models
from db import models_function
from .db_func import db

from os.path import isfile


def init_db():
    if not isfile(SQLITE_FILE_PATH):
        print('[ init DB ]')
        create_db()
        fill_users()


def create_db():
    db.generate_db(models.Base)


def fill_users():
    for i in range(4):
        num = i+1
        models_function.add_user('User' + str(num), str(num + 1234))

    models_function.add_user('Weller', 'qwerty')
    models_function.add_user('User6', 'C02MN0FNG083')
    models_function.add_user('User7', 'C02MN0FNG083')


if __name__ == '__main__':
    init_db()