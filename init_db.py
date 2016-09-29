import models
import models_function

from db_func import db


def create_db():
    db.generate_db(models.Base)


def fill_users():
    for i in range(10):
        models_function.add_user('User'+str(i))


if __name__ == '__main__':
    create_db()
    fill_users()