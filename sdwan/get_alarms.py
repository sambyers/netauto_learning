import json
import sys
from yaml import safe_load
from sdwan import Sdwan


config_file = sys.argv[1]
with open(config_file) as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)
response = api.devicestate.get_alarms()
print(json.dumps(response['data'], indent=2))