__author__ = "Jeremy Nelson"
import falcon

from . import Repository

class FedoraObject(Repository):

    def on_get(self, req, resp, pid):
        output = {"message": "Should Display Fedora Object {}".format(pid)}
        resp.body = str(output)
        resp.status = falcon.HTTP_200
