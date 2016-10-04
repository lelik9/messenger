# coding=utf-8
import time

from kivy.app import App
from kivy.network.urlrequest import UrlRequest


class Api(object):
    server = 'http://127.0.0.1:8887'

    def __init__(self, url, method, callback, **kwargs):
        methods = {
            'GET': self.get,
            'POST': self.post
        }
        self.callback = callback
        try:
            request = methods[method]
            request(url, **kwargs)
        except KeyError:
            raise KeyError('method not found, use "GET" or "POST"')

    def get(self, url, **kwargs):
        params = '&'.join(['='.join([k, v]) for k, v in kwargs])
        full_url = self.server + url + '?' + params
        UrlRequest(url=full_url, on_success=self.on_success, on_error=self.on_error,
                   on_failure=self.on_error)

    def post(self, url, **kwargs):
        full_url = self.server + url
        UrlRequest(url=full_url, on_success=self.on_success, on_error=self.on_error,
                   on_failure=self.on_error, req_body=kwargs)

    def on_error(self, err):
        print('server error {}'.format(str(err)))

    def on_success(self, req, response):
        print('server response: ', response)
        self.callback(response)


class UserApi(object):
    user_id = 1

    @staticmethod
    def create_chat(name, chat_type, users, callback):
        def chat_callback(response):
            callback()

        Api(url='/group/', method='POST', callback=chat_callback, group_name=name,
            group_type=chat_type, users=users)

    @classmethod
    def send_message(cls, chat_id, message, callback):
        def message_callback(response):
            callback()

        Api(url='/message/', method='POST', callback=message_callback, user=cls.user_id,
            chat_id=chat_id, message=message)

    @classmethod
    def update_message(cls, callback):
        def update_callback(response):
            callback()

        Api(url='/message/', method='GET', callback=update_callback, user=cls.user_id)

    @classmethod
    def get_message_range(cls, chat_id, message_id, range, callback):
        def range_callback(response):
            callback()

        Api(url='/message/range/', method='GET', callback=range_callback, chat_id=chat_id,
            user=cls.user_id, last_message=message_id, range=range)

    @classmethod
    def get_users_list(cls, callback):
        def users_callback(response):
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

        Button:
            id: login_button
            size_hint: 1, None
            size: root.width, '40dp'
            text: 'VK login'
            on_press: root.login()

        Button:
            id: join_button
            size_hint: 1, None
            size: root.width, '40dp'
            text: 'VK join group'
            on_press: root.join()
"""

Builder.load_string(main_widget)


class MainWidget(Widget):
    def __init__(self, *args, **kwargs):
        super(MainWidget, self).__init__(*args, **kwargs)
        # Create private room
        Api(url='group/?', method='POST', callback=None, group_name='api_test1',
            group_type='private', users='1,2')

        # Create group room
        Api(url='group/?', method='POST', callback=None, group_name='api_test2',
            group_type='group', users='1,2')


if __name__ == '__main__':
    class MainApp(App):
        def build(self):
            return MainWidget()


    MainApp().run()
