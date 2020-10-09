from dnac import DNAC
import json


with open('host.json', 'r') as f:
    host = json.loads(f.read())

dnac = DNAC(**host)
data = dnac.get_discoveries_by_range(1, 10)
print(json.dumps(data, indent=2))