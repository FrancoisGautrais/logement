import json


from pyquery import PyQuery as pq

from logement.libs.scrapper.base.request import Get


class Connector:

    def __init__(self):
        self.url = None

    # def from_url(self, url):
    #     raise NotImplementedError()
    #

    def from_request(self, req):
        raise NotImplementedError()

    def cast(self, data):
        raise NotImplementedError()



class HtmlConnector(Connector):

    def from_request(self, req):
        if isinstance(req, str):
            req = Get(req)
        return req().pq

    def cast(self, data):
        return pq(data)


class JsonConnector(Connector):

    def from_request(self, req):
        if isinstance(req, str):
            req = Get(req)
        return req().json

    def cast(self, data):
        return data