from sdwan import Sdwan
from yaml import safe_load
import json


with open('config.yml') as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)

device_templates = api.get_device_templates()
site1_device_template = next(d for d in device_templates['data'] if d['templateName'] == 'Site_3_vEdge_Template')
print(json.dumps(site1_device_template, indent=2))