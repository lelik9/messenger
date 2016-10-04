# coding=utf-8
import json
import time
import urllib

from kivy.app import App
from kivy.network.urlrequest import UrlRequest


def on_error(req, err):
    print('server error {}'.format(str(err)))


class Api(object):
    server = 'http://127.0.0.1:8887'

    def __init__(self, url, method, callback, **kwargs):
        methods = {
            'GET': self.get,
            'POST': self.post
        }
        self.header = {'Content-type': 'application/x-www-form-urlencoded',
                       'Accept': 'text/plain'}
        self.callback = callback

        try:
            request = methods[method]
            request(url, **kwargs)
        except KeyError:
            raise KeyError('method not found, use "GET" or "POST"')

    def get(self, url, **kwargs):
        params = '&'.join(['='.join([k, v]) for k, v in kwargs.items()])
        full_url = self.server + url + '?' + params
        UrlRequest(url=full_url, on_success=self.callback, on_error=on_error,
                   on_failure=on_error)

    def post(self, url, **kwargs):
        full_url = self.server + url
        params = urllib.urlencode(kwargs)

        UrlRequest(url=full_url, on_success=self.callback, on_error=on_error,
                   on_failure=on_error, req_body=params, req_headers=self.header)


class UserApi(object):
    user_id = '2'

    @staticmethod
    def create_chat(name, chat_type, users, callback):
        def chat_callback(req, response):
            print('server response: ', response)
            if response['type'] == 'error':
                on_error(req, response['result'])
            callback()

        Api(url='/group/', method='POST', callback=chat_callback, group_name=name,
            group_type=chat_type, users=users)

    @classmethod
    def set_delivered(cls,chat_id, message_id):
        pass
    @classmethod
    def send_message(cls, chat_id, message, callback):
        def message_callback(req, response):
            print('server response: ', response)
            if response['type'] == 'error':
                on_error(req, response['result'])
            callback()

        Api(url='/message/', method='POST', callback=message_callback, user=cls.user_id,
            chat_id=chat_id, message=message)

    @classmethod
    def update_message(cls, callback):
        def update_callback(req, response):
            print('server response: ', response)
            if response['type'] == 'error':
                on_error(req, response['result'])
            callback()

        Api(url='/message/', method='GET', callback=update_callback, user=cls.user_id)

    @classmethod
    def get_message_range(cls, chat_id, message_id, range, callback):
        def range_callback(req, response):
            print('server response: ', response)
            if response['type'] == 'error':
                on_error(req, response['result'])
            callback()

        Api(url='/message/range/', method='GET', callback=range_callback, chat_id=chat_id,
            user=cls.user_id, last_message=message_id, range=range)

    @classmethod
    def get_users_list(cls, callback):
        def users_callback(req, response):
            print('server response: ', response)
            if response['type'] == 'error':
                on_error(req, response['result'])
            callback()
            time.sleep(600)
            cls.get_users_list(callback)

        Api(url='/users/', method='GET', callback=users_callback, user=cls.user_id)


from kivy.lang import Builder
from kivy.uix.widget import Widget

main_widget = """
<MainWidget>:
    BoxLayout:
        id: control_panel
        orientation: 'vertical'
        size_hint: 1, 1
        size: root.width, root.height

"""

Builder.load_string(main_widget)


class MainWidget(Widget):
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)
        # Create private room
        # UserApi.create_chat('api-test1', 'private', '1,2', None)

        # Create group room
        # UserApi.create_chat('api-test2', 'group', '3,5,7', None)
        # UserApi.update_message(None)
        # UserApi.send_message('1', 'test2', None)
        UserApi.update_message(None)

if __name__ == '__main__':
    class MainApp(App):
        def build(self):
            return MainWidget()


    MainApp().run()
