import json
from pyquery import PyQuery as pq
import requests


class Request:

    def __init__(self, method, url, data=None, headers=None, **kwargs):
        self.method = method
        self.url = url
        self.data = data
        self.headers = headers
        self.kwargs = kwargs
        self.response = None


    def __call__(self, *args, **kwargs):
        if self.data:
            kwargs["data"]=self.data
        if self.headers:
            kwargs["headers"]=self.headers
        self.response =  requests.request(self.method.upper(), self.url, **kwargs)
        return self

    @property
    def content(self):
        return self.response.content if self.response else None

    @property
    def pq(self):
        return pq(self.response.content) if self.response else None

    @property
    def status(self):
        return self.response.status_code if self.response else None

    def __bool__(self):
        return self.response and  0 < self.response.status_code < 400

    @property
    def json(self):
        try:
            if self.response and self.response.content:
                return json.loads(self.response.content)
        except json.decoder.JSONDecodeError:
            pass
        return None


class Get(Request):
    def __init__(self, url, data=None, headers=None, **kwargs):
        super().__init__("GET", url, data, headers, **kwargs)

class Post(Request):
    def __init__(self, url, data=None, headers=None, **kwargs):
        super().__init__("POST", url, data, headers, **kwargs)
