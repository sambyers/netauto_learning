import json
import sys
from yaml import safe_load
from sdwan import Sdwan


config_file = sys.argv[1]

try:
    templateid = sys.argv[2]
except(IndexError):
    templateid = None

with open(config_file) as fh:
    config = safe_load(fh.read())

s = Sdwan(**config, verify_tls=False)

response = s.deviceconfiguration.get_device_templates()
print(json.dumps(response['data'], indent=2))

if templateid:
    response = s.deviceconfiguration.get_device_template_object(templateid)
    print(json.dumps(response, indent=2))