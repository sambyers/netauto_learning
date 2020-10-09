from dnac import DNAC
import json
from sys import argv

with open('host.json', 'r') as f:
    host = json.loads(f.read())

dnac = DNAC(**host)
id = argv[1]
devices = dnac.get_device_by_id(id)
print(json.dumps(devices, indent=2))