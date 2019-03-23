import requests


class HttpClient:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {}

    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    def post(self, url, data, json = None, **kwargs):
        return self.session.post(url, data, json, **kwargs)
