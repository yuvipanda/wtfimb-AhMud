from lxml import etree
from urllib2 import urlopen
from pylinq import PyLINQ
import simplejson as json
import sys

SWIVT_NAMESPACE = "http://semantic-mediawiki.org/swivt/1.0#"
RDF_NAMESPACE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS_NAMESPACE = "http://www.w3.org/2000/01/rdf-schema#"
PROPERTY_NAMESPACE = "http://wiki.busroutes.in/wiki/Special:URIResolver/Property-3A"
NAMESPACES = {
    'swivt': SWIVT_NAMESPACE, 
    'rdf': RDF_NAMESPACE, 
    'rdfs': RDFS_NAMESPACE,
    'property': PROPERTY_NAMESPACE
}

TRAIN_CAT_URL = "http://wiki.busroutes.in/wiki/Special:ExportRDF/Category:Train_route"

def get_doc(url):
    return etree.parse(urlopen(url))

def get_route_data(route_url):
    route_doc = get_doc(route_url)
    subject_node = route_doc.xpath('//swivt:Subject[rdfs:isDefinedBy[@rdf:resource="'+route_url+'"]]', namespaces=NAMESPACES)[0]
    label = subject_node.xpath('rdfs:label', namespaces=NAMESPACES)[0].text

    stops = subject_node.xpath('property:Stops_at/@rdf:resource', namespaces=NAMESPACES)
    stop_urls = [route_doc.xpath('//swivt:Subject[@rdf:about="' + stop + '"]/rdfs:isDefinedBy/@rdf:resource', namespaces=NAMESPACES)[0] for stop in stops]
    stop_tuples = [get_stop_data(stop_url) for stop_url in stop_urls]
    return (label, stop_tuples)

def get_stop_data(stop_url):
    stop_doc = get_doc(stop_url)
    subject_node = stop_doc.xpath('//swivt:Subject[rdfs:isDefinedBy[@rdf:resource="'+stop_url+'"]]', namespaces=NAMESPACES)[0]
    display_name = subject_node.xpath('property:Display_name', namespaces=NAMESPACES)[0].text
    located_at = subject_node.xpath('property:Located_at', namespaces=NAMESPACES)
    if located_at:
        located_at = located_at[0].text
    else:
        located_at = "No Location Data"
    return (display_name, located_at)

trains_doc = get_doc(TRAIN_CAT_URL)
trains = PyLINQ(trains_doc.xpath('//swivt:Subject[rdf:type[@rdf:resource="http://wiki.busroutes.in/wiki/Special:URIResolver/Category-3ATrain_route"]]/rdfs:isDefinedBy/@rdf:resource', namespaces=NAMESPACES)).distinct(lambda x: x).items()

json.dump([get_route_data(train) for train in trains], sys.stdout, indent=4, sort_keys=True)
