import csv

routes_reader = csv.DictReader(open("routes.csv"))
routes = dict([(r["name"],[]) for r in routes_reader])

stages_reader = csv.DictReader(open("stages.csv"))
stages = dict([(r["name"], r) for r in stages_reader])

route_stages_reader = csv.DictReader(open("routestages.csv"))
for rs in route_stages_reader:
    routes[rs['route_name']].append((rs['stop_name'], rs['sequence']))

for rname in routes:
    routes[rname] = [r[0] for r in sorted(routes[rname], key=lambda x: x[1])]
 
print routes
