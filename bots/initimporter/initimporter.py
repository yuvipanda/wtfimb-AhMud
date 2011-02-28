import csv
from jinja2 import Template

routes_reader = csv.DictReader(open("routes.csv"))
routes = dict([(r["name"],[]) for r in routes_reader])

stops_reader = csv.DictReader(open("stops.csv"))
stops = dict([(r["name"], r) for r in stops_reader])

route_stops_reader = csv.DictReader(open("routestops.csv"))
for rs in route_stops_reader:
    routes[rs['route_name']].append((rs['stop_name'], rs['sequence']))

for rname in routes:
    routes[rname] = [r[0] for r in sorted(routes[rname], key=lambda x: x[1])]

route_template = Template(open('route.template').read())
stop_template = Template(open('stop.template').read())

for r in routes:
    up = route_template.render(route={'stops': routes[r]})
    down = route_template.render(route={'stops': reversed(routes[r])})

for s in stops:
    stop = stop_template.render(stop=stops[s])
    print stop
    raw_input()

print routes
