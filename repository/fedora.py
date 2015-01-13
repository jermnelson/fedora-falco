__author__ = "Jeremy Nelson"
import falcon

class Resource(object):
    """Fedora Resource wrapper, see 
    https://wiki.duraspace.org/display/FEDORA40/Glossary#Glossary-Resource

    >> import fedora
    >> resource = Resource() # Default wrapper for Fedora at http://localhost:8080
    """

    def on_get(self, req, resp):
        """HTTP GET Method response, returns JSON, XML, N3, or Turtle representations

	Args:
	    req - HTTP Request
	    resp - HTTP Response
        """
        resp.body = '{"graph": "Sample graph"}'
        resp.status = falcon.HTTP_200
