"""A Fedora Repository Foxml parser for decomposing Fedora 2.4 compound objects
into individual Fedora 3.7 objects"""
__author__ = "Jeremy Nelson"

import falcon
import rdflib
from jinja2 import Template
try:
    import xml.etree.cElementTree as etree
except ImportError:
    import xml.etree.ElementTree as etree
from ...resources.fedora3 import ISLANDORA_CONTENT_MODELS, NAMESPACES

FOXML_TEMPLATE = Template("""<foxml:digitalObject VERSION="1.1" PID="{{ pid }}"
 xmlns:foxml="info:fedora/fedora-system:def/foxml#"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="info:fedora/fedora-system:def/foxml#
 http://www.fedora.info/definitions/1/0/foxml1-1.xsd">
 {% if objectProperties %}{{ objectProperties }}{% endif %}
 {% if marcDatastream %}{{ marcDatastream }}{% endif %}
 {% if auditDatastream %}{{ auditDatastream }}{% endif %}
 {% if policyDatastream %}{{ policyDatastream }}{% endif %}
 {% if modsDatastream %}{{ modsDatastream }}{% endif %}
 {% if dcDatastream %}{{ dcDatastream }}{% endif %}
 {% if dissXmlDatastream %}{{ dissXmlDatastream }}{% endif %}
 <foxml:datastream ID="RELS-EXT" STATE="A" CONTROL_GROUP="X" VERSIONABLE="true">
    <foxml:datastreamVersion ID="RELS-EXT.0" LABEL="RDF Statements about this Object" MIMETYPE="application/rdf+xml">
       <foxml:xmlContent>
        <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
          xmlns:fedora="info:fedora/fedora-system:def/relations-external#"
          xmlns:fedora-model="info:fedora/fedora-system:def/model#"
          xmlns:islandora="http://islandora.ca/ontology/relsext#">
          <rdf:Description rdf:about="info:fedora/{{ pid }}">
            <fedora:isMemberOfCollection rdf:resource="info:fedora/{{ collectionPid }}"/>
            <fedora-model:hasModel rdf:resource="info:fedora/{{ contentModel }}" />
          </rdf:Description>
        </rdf:RDF>
       </foxml:xmlContent>
    </foxml:datastreamVersion>
 </foxml:datastream>
</foxml:digitalObject>""")


class FoxmlContentHandler(object):

    EXCLUDED_TAILS  = [
        ".xml",
        ".jp2",
        "-tn.jpg",
        "TN",
        ".swf",
        "DISS_XML",
        "-access.mp3",
        "lg.jpg",
        "sm.jpg"]
    SAVED_DATASTREAMS = [
            "RELS-EXT",
            "AUDIT",
            "POLICY",
            "DC",
            "MODS",
            "MARC",
            "DISS_XML"]

    def __init__(self, source_filepath):
        self.foxml_filepath = source_filepath
        self.info = {}

    def _exclude(self, fedora_object):
        for tail in FoxmlContentHandler.EXCLUDED_TAILS:
            if fedora_object.endswith(tail):
                return True
        return False

    def _process_ds(self, datastream):
        """Helper Method processes datastreams"""
        ds_type = datastream.attrib.get("ID")
        if ds_type in FoxmlContentHandler.SAVED_DATASTREAMS:
            if not ds_type.lower() in self.info:
                self.info[ds_type.lower()] = datastream
        elif ds_type.startswith("RELS-INT"):
            pass
        else:
            if not self._exclude(ds_type):
                self.info["master-object"] = datastream

    def parse(self):
        context = etree.iterparse(open(self.foxml_filepath), events=('end',))
        collection = None
        for action, elem in context:
            tag = str(elem.tag)
            if tag.endswith("datastream"):
                self._process_ds(elem)
            elif tag.endswith("digitalObject"):
                    if not "pid" in self.info:
                        self.info['pid'] = elem.attrib.get('PID')
                    if not "version" in self.info:
                        self.info["version"] = elem.attrib.get('VERSION')
            elif tag.endswith("hasModel"):
                if not "content_model" in self.info:
                    self.info["content_model"] = elem.attrib.get(
                        "{{{0}}}resource".format(rdflib.RDF))
            elif tag.endswith("contentLocation"):
                if not "content_location" in self.info:
                    self.info["content_location"] = elem.attrib.get('REF')
            elif tag.endswith("isMemberOfCollection") or tag.endswith("isMemberOf"):
                if not "collection" in self.info:
                    collection = elem.attrib.get(
                        "{{{0}}}resource".format(rdflib.RDF))
                    if len(collection) > 0:
                        self.info['collection'] = collection
            elif tag.lower().endswith("description"):
                fedora_object = elem.attrib.get(
                    "{{{0}}}about".format(rdflib.RDF))
                if fedora_object:
                    if self._exclude(fedora_object):
                        continue
                    if 'object-ids' in self.info:
                        self.info['object-ids'].append(fedora_object)
                    else:
                        self.info['object-ids'] = [fedora_object, ]
            elif tag.endswith("objectProperties"):
                self.info["obj_properties"] = elem
        print("Fedora info {}".format(
            self.info))












