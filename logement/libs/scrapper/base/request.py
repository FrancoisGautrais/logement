import json
from pathlib import Path

from pyquery import PyQuery as pq
import requests

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
class Request:

    def __init__(self, method, url, data=None, headers=None, **kwargs):
        self.method = method
        self.url = url
        self.data = data
        self.headers = headers or {}
        self.kwargs = kwargs
        self.response = None


    def __call__(self, *args, **kwargs):
        kwargs.update(self.kwargs)
        if self.data:
            kwargs["data"]=self.data
        if self.headers:
            kwargs["headers"]=self.headers
        if kwargs.get("headers", {}).get("User-Agent") is None:
            kwargs["headers"] = kwargs.get("headers", {})
            kwargs["headers"]["User-Agent"]="Mozilla/5.0 (X11; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0"

        self.response = requests.request(self.method.upper(), self.url,  **kwargs)

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
