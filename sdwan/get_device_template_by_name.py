import json
import sys
from yaml import safe_load
from sdwan import Sdwan


config_file = sys.argv[1]
template_name = sys.argv[1]

with open(config_file) as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)

device_templates = api.deviceconfiguration.get_device_templates()
site1_device_template = next(d for d in device_templates['data'] if d['templateName'] == template_name)
print(json.dumps(site1_device_template, indent=2))