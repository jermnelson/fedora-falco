__author__ = "Jeremy Nelson"
import falcon
from . import Repository


class Resource(Repository):
    """Fedora Resource wrapper, see
    https://wiki.duraspace.org/display/FEDORA40/Glossary#Glossary-Resource

    >> import fedora
    >> resource = fedora.Resource()
    """

    def on_delete(self, req, resp, id, predicate=None, object_=None):
        pass

    def on_get(self, req, resp, id):
        """GET Method response, returns JSON, XML, N3, or Turtle representations

	    Args:
            req -- Request
            resp -- Response
	        id -- A unique ID for the Resource, should be UUID
        """
        pass

    def on_patch(self, req, resp, id, sparql):
        pass

    def on_post(self, req, resp, id=None):
        pass

    def on_put(self, req, resp, id):
        """PUT method takes an id, a list of predicate and object tuples and
        updates Repository

        Args:
            req -- Request
            resp -- Response
            id -- Unique ID for the Resource
        """
        fedora_url = self.search.query(id)

        fedora_url_request = urllib.request.Request(
            fedora_url,
            data=sparql.encode(),
            method='PATCH',
            headers={'Content-Type': 'application/sparql-update'}
        )
        if self.opener:
            result = self.opener(fedora_url_request)
        else:
            result = urllib.request.urlopen(fedora_url_request)
        return True



class Transaction(Repository):

    def on_get(self, req, resp, token=None):
        pass
