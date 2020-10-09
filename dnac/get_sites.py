from dnac import DNAC
import json
from sys import argv

with open('host.json', 'r') as f:
    host = json.loads(f.read())

dnac = DNAC(**host)

count = dnac.get_site_count()
print(json.dumps(count, indent=2))

if len(argv) > 1:
    # Send query params in request to DNAC for only sites in the site hierarchy supplied as argument to script
    body = {'name': argv[1]}
else:
    body = None


data = dnac.get_site(body)
print(json.dumps(data, indent=2))