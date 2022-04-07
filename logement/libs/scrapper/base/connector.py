import json

import requests
from pyquery import PyQuery as pq

class Connector:

    def __init__(self):
        self.url = None

    def from_url(self, url):
        raise NotImplementedError()

    def cast(self, data):
        raise NotImplementedError()



class HtmlConnector(Connector):

    def from_url(self, url):
        return pq(url=url)

    def cast(self, data):
        return pq(data)


class JsonConnector(Connector):

    def from_url(self, url):
        x = requests.get(url)
        if x.status_code<400:
            try:
                return json.loads(x.content)
            except:
                pass
        return None

    def cast(self, data):
        return data