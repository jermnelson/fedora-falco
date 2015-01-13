__author__ = "Jeremy Nelson"

import falcon

from repository.fedora import Resource, Transaction
from repository.fedora3 import FedoraObject
from werkzeug.serving import run_simple
api = application = falcon.API()

api.add_route("/Resource/{id}", Resource())
api.add_route("/Transaction", Transaction())
api.add_route("/Object/{pid}", FedoraObject())

if __name__ == '__main__':
    run_simple('0.0.0.0', 9001, application, use_reloader=True)