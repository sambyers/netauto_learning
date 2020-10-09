from dnac import DNAC
import json


command_runner_job = {
    "commands": [ "show ver" ],
    "deviceUuids": [ "1cfd383a-7265-47fb-96b3-f069191a0ed5" ]
}

with open('host.json', 'r') as f:
    host = json.loads(f.read())

dnac = DNAC(**host)
data = dnac.create_command_runner(command_runner_job)
print(json.dumps(data, indent=4))