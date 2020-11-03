import json
import sys
from yaml import safe_load
from sdwan import Sdwan


config_file = sys.argv[1]
with open(config_file) as fh:
    config = safe_load(fh.read())

s = Sdwan(**config, verify_tls=False)
response = s.deviceconfiguration.get_device_templates()
print(json.dumps(response['data'], indent=2))