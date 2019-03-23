from requests import Session
from requests.cookies import merge_cookies


class HttpClient:
    def __init__(self):
        self.__session = Session()

    def get(self, url, **kwargs):
        return self.__session.get(url, **kwargs)

    def post(self, url, data, json = None, **kwargs):
        return self.__session.post(url, data, json, **kwargs)

    def get_headers(self):
        return self.__session.headers

    def set_headers(self, k, v):
        self.__session.headers[k] = v

    def get_cookies(self):
        return self.__session.cookies

    def set_cookies(self, cookies):
        self.__session.cookies = merge_cookies(self.__session.cookies, cookies)

