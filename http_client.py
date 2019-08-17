from requests import Session
from requests.cookies import merge_cookies


class HttpClient:
    def __init__(self):
        self.__session = Session()

    def get(self, url, **kwargs):
        return self.__session.get(url, **kwargs)

    def post(self, url, data, json = None, **kwargs):
        return self.__session.post(url, data, json, **kwargs)

    def delete(self, url, **kwargs):
        return self.__session.delete(url, **kwargs)

    def put(self, url, data, **kwargs):
        return self.__session.put(url, data, **kwargs)

    def get_headers(self):
        return self.__session.headers

    def set_headers(self, k, v):
        self.__session.headers[k] = v

    def get_cookies(self):
        return self.__session.cookies

    def set_cookies(self, cookies):
        # from requests.cookies import RequestsCookieJar
        # url = "http://fanyi.baidu.com/v2transapi"
        # cookies = RequestsCookieJar()
        # cookies.set("BAIDUID", "B1CCDD4B4BC886BF99364C72C8AE1C01:FG=1", domain="baidu.com")
        self.__session.cookies = merge_cookies(self.__session.cookies, cookies)

    def get_auth(self):
        return self.__session.auth

    def set_auth(self, auth):
        # from requests.auth import HTTPBasicAuth
        # auth=HTTPBasicAuth('user', 'pass')
        self.__session.auth = auth

    def set_proxy(self, proxies):
        # proxies = {'http': 'http://localhost:8888', 'https': 'http://localhost:8888'}
        self.__session.proxies = proxies

    def get_proxy(self):
        return self.__session.proxies

    def close(self):
        self.__session.close()

