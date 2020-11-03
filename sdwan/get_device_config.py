import json
import sys
from yaml import safe_load
from sdwan import Sdwan


config_file = sys.argv[1]
deviceid = sys.argv[2]

with open(config_file) as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)
resp = api.deviceconfiguration.get_attached_config(deviceid)
print(json.dumps(resp, indent=2))