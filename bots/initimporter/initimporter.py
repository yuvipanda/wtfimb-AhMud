import csv
from jinja2 import Template
import mwclient
import sys

try:
    import settings
    site = mwclient.Site(settings.host_name, settings.site_path)
    site.login(settings.username, settings.password)
except ImportError:
    print "Cannot find settings.py"
    sys.exit(-1)

routes_reader = csv.DictReader(open("routes.csv"))
routes = dict([(r["name"],[]) for r in routes_reader])

stops_reader = csv.DictReader(open("stops.csv"))

stops_unsanitized = dict([(r["name"], r) for r in stops_reader])
stops = {}

def sanitize(ip):
    return ip.replace(";","")

for sname in stops_unsanitized:
    sanitized_name = sanitize(sname)
    stops[sanitized_name] = stops_unsanitized[sname]
    stops[sanitized_name]["name"] = sanitized_name

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
    page = site.pages[settings.city_prefix + stops[s]["name"]]
    text = page.edit()
    if text == "":
        page.save(stop, summary="Import from old bri data")
    else:
        print "stop '%s' exists already. Not overwriting" % stops[s]["name"]
