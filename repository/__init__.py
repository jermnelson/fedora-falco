"""Module wraps Fedora Commons repository, Elasticsearch, and Fuseki
into single API for use in such projects as the BIBFRAME Catalog, TIGER Catalog,
Islandora eBadges, Schema.org Editor, and Django BFE projects.
"""
__author__ = "Jeremy Nelson"

import falcon
import urllib.request

from elasticsearch import Elasticsearch
from .fuseki import Fuseki


class Repository(object):
    """Base repository object"""

    def __init__(self, **kwargs):
        """Initializes a Repository object.

        Keyword arguments:
            es -- Elastic search instance, default is http://localhost:9200
            fuseki -- Fuseki instance, default is http://localhost:3030
            fedora -- Fedora 4 REST url, default is http://localhost:8080/rest/
            fedora3 -- Fedora 3.+ url, default is
            admin_user -- Fedora Administrator, defaults to None
            admin_pwd -- Fedora Password, defaults to None
        """
        self.fedora = kwargs.get('fedora', None)
        self.fedora3 = kwargs.get('fedora3', None)
        self.search = kwargs.get('es', Elasticsearch())
        self.triple_store = kwargs.get('fuseki', Fuseki())
        if self.fedora and self.fedora3:
            raise ValueError("Cannot initialize both Fedora 3.+ {} and "\
                             "Fedora 4 {} in the same repository".format(
                             self.fedora3,
                             self.fedora))
        # Default is a Fedora 4 repository
        if not self.fedora and not self.fedora3:
            self.fedora = "http://localhost:8080/rest/"
        admin = kwargs.get('admin_user', None)
        admin_pwd = kwargs.get('admin_pwd', None)
        self.opener = None
        # Create a Password manager
        if admin and admin_pwd:
            password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(
                None,
                self.fedora,
                admin,
                admin_pwd)
            handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
            self.opener = urllib.request.build_opener(handler)


