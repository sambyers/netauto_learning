import json
import sys
from yaml import safe_load
from sdwan import Sdwan


config_file = sys.argv[1]
templateid = sys.argv[2]

with open(config_file) as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)

device_template_object = api.deviceconfiguration.get_device_template_object(templateid)
print(json.dumps(device_template_object, indent=2))