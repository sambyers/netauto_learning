from sdwan import Sdwan
from yaml import safe_load
import json


with open('alwayson_config.yml') as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)
response = api.devicestate.get_alarms()
print(json.dumps(response['data'], indent=2))