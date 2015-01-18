__author__ = "Jeremy Nelson"
import falcon

from .. import Repository

NAMESPACES ={
    "foxml": "info:fedora/fedora-system:def/foxml#"
}

class FedoraObject(Repository):

    def on_get(self, req, resp, pid):
        output = {"message": "Should Display Fedora Object {}".format(pid)}
        resp.body = str(output)
        resp.status = falcon.HTTP_200

    def migrate_to(self, target_repository):
        """Method migrates Object to a target repository

        Args:
            target_repository -- Fedora Repository 3.7 or 3.8 repository
        """
        pass



