"""A Fedora Repository Foxml parser for decomposing Fedora 2.4 compound objects
into individual Fedora 3.7 objects"""
__author__ = "Jeremy Nelson"

import falcon
import rdflib
try:
    import xml.etree.cElementTree as etree
except ImportError:
    import xml.etree.ElementTree as etree
from ...resources.fedora3 import NAMESPACES

class FoxmlContentHandler(object):
    xpath_v = "/".join([
        "{{{0}}}datastreamVersion[last()]",
        "{{{0}}}xmlContent",
        "{{{1}}}RDF"])

    def __init__(self, source_filepath):
        self.foxml_filepath = source_filepath

    def _process_ds(self, datastream):
        """Helper Method processes datastream"""
        ds_type = datastream.attrib.get("ID")
        if ds_type.startswith("RELS-EXT"):
            #self._process_rels_ext(datastream)
            pass
        if ds_type.startswith('AUDIT'):
            pass
##        for snippet in [
##            "{{{1}}}Description/{{{0}}}isMemberOfCollection",
##            "{{{1}}}description/{{{0}}}isMemberOfCollection",
##            ]:
##                xpath = "{}/{}".format(FoxmlContentHandler.xpath_v, snippet)
##                print(xpath.format(
##                        NAMESPACES.get('foxml'),
##                        rdflib.RDF))
##                element = datastream.find(
##                    xpath.format(
##                        NAMESPACES.get('foxml'),
##                        rdflib.RDF))
##                print("ELement is {}".format(element))
##                if element:
##                    collection = element.attrib.get(
##                        "{{{0}}}resource".format(rdflib.RDF))
##                    break
        print("In Process RELS-EXT method collection is {}".format(collection))


    def parse(self):
        context = etree.iterparse(open(self.foxml_filepath), events=('end',))
        collection = None
        for action, elem in context:
            if elem.tag == "{{{0}}}datastream".format(NAMESPACES.get('foxml')):
                self._process_ds(elem)
            if elem.tag == "{{{0}}}digitalObject".format(
                NAMESPACES.get('foxml')):
                    version = elem.attrib.get('VERSION')
                    pid = elem.attrib.get('PID')
            if str(elem.tag).endswith("isMemberOfCollection"):
                if collection:
                    pass
                print(elem.attrib, "{{{0}}}resource".format(rdflib.RDF))
                collection = elem.attrib.get(
                    "{{{0}}}resource".format(rdflib.RDF))
                print(collection)


        print("Fedora {} version is {} and collection is ".format(
            pid,
            version,
            collection))


##    def startElement(self, name, attrs):
##        if name == "foxml:datastream":
##            if 'ID' in attrs:
##                self.datastream_type = attrs.getValue('ID')
##            if _id.startswith('AUDIT'):
##                self.process_audit()
##            if _id.startswith('POLICY'):
##                self.process_policy()
##            if _id.startswith('DC'):
##                self.process_dublin_Core()
##            if _id.startswith('MODS'):
##                self.process_mods()
##            if _id.startswith('MARC'):
##                self.process_marc()












