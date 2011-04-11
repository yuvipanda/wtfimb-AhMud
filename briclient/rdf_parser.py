import sys

import logging
_logger = logging.getLogger("rdflib")
_logger.setLevel(logging.ERROR)
_hdlr = logging.StreamHandler()
_hdlr.setFormatter(logging.Formatter('%(name)s %(levelname)s: %(message)s'))
_logger.addHandler(_hdlr)

import rdflib
from rdflib import Graph, URIRef

rdflib.plugin.register('sparql', rdflib.query.Processor,
                       'rdfextras.sparql.processor', 'Processor')
rdflib.plugin.register('sparql', rdflib.query.Result,
                       'rdfextras.sparql.query', 'SPARQLQueryResult')

def print_usage():
    print "Usage: python %s <path_to_rdf_file>" % sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print_usage()
        sys.exit()
    g = Graph()
    g.parse(sys.argv[1])
    
    # Proof-of-concept print all train_routes
    print "Train routes:"
    print "============="
    for train_route_uri, train_route_name in g.query('select ?p ?name where { ?p rdfs:label ?name . ?p rdf:type wiki:Category-3ATrain_route }', initNs=dict(g.namespaces())):
        print train_route_name
        print '-' * len(train_route_name)
        for train_stop in g.query('select ?name where { ?train_route property:Stops_at ?o . ?o rdf:type wiki:Category-3ATrain_stop . ?o property:Display_name ?name }', initNs=dict(g.namespaces()), initBindings={'train_route': URIRef(train_route_uri)}):
            print train_stop
        print
    
    # Print segment stops(with sequence)
    print "Segments:"
    print "========="
    for segment_uri, segment_label in g.query('select ?p ?name where { ?p rdfs:label ?name . ?p rdf:type wiki:Category-3ASegment }', initNs=dict(g.namespaces())):
        print segment_label
        print '-' * len(segment_label)
        results = list(g.query('select ?stop_name ?sequence where { ?ss property:Stop_segment ?segment . ?ss property:Stop ?stop . ?stop property:Display_name ?stop_name . ?ss property:Sequence ?sequence }', initNs=dict(g.namespaces()), initBindings={'segment':URIRef(segment_uri)}))
        sorted_results = sorted(results, key=lambda x: x[1])
        for stop_name, sequence in sorted_results:
            print sequence, stop_name
        print
