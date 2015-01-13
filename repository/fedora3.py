__author__ = "Jeremy Nelson"
import falcon

class FedoraObject(object):

    def on_get(self, req, resp):
        resp.body = ''
