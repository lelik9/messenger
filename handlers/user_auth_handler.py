# coding=utf-8
import tornado.web

from db import models_function
from handlers.handler import write


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class LoginHandler(BaseHandler):
    def get(self):
        self.render('../template/login.html', error=None)

    def post(self):
        user = self.get_argument("name")
        password = self.get_argument("password")

        if user == 'admin':
            if password == 'admin':
                self.set_secure_cookie("user", user)
                self.redirect(self.get_argument("next", "/"))
        else:
            self.render("../template/login.html", error="incorrect password or login")


class UserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        """
        Return users list
        """
        users = models_function.get_users_list()
        self.render('../template/user.html', users=users)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        """
        Register new user
        """
        user_uuid = self.get_argument('user_uuid')
        user_name = self.get_argument('user_name')

        user = models_function.add_user(user_name, user_uuid)

        if not user:
            self.send_error(500)
        else:
            self.redirect('/')


class UserAuthHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        """
        First user entrance
        """
        user_uuid = self.get_argument('uuid')

        token = models_function.get_user_token(uuid=user_uuid)

        if token:
            write(req=self, msg_type='success', msg={'token': token[0], 'id': token[1]})
        else:
            write(req=self, msg_type='error', msg='User not register')


class DeleteUserHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        user_id = self.get_argument('user_id')

        result = models_function.mark_delte_user(user_id=user_id)

        if not result:
            self.send_error(500)
        else:
            self.redirect('/')
