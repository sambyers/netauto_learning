from dnac import DNAC
import json


with open('host.json', 'r') as f:
    host = json.loads(f.read())

dnac = DNAC(**host)
data = dnac.get_command_runner_accepted_cli()
print(json.dumps(data, indent=4))