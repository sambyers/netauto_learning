from dnac import DNAC
import json

with open('host.json', 'r') as f:
    host = json.loads(f.read())

dnac = DNAC(**host)
event_subs = dnac.get_events()
print(json.dumps(event_subs, indent=4))