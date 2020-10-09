from dnac import DNAC
import json


with open('host.json', 'r') as f:
    host = json.loads(f.read())

dnac = DNAC(**host)

# Get all sites' health
data = dnac.get_site_health()
print(json.dumps(data, indent=2))