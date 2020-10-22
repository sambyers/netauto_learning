from sdwan import Sdwan
from yaml import safe_load
import json


with open('config.yml') as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)

device_templates = api.get_device_templates()
device_template = next(d for d in device_templates['data'] if d['templateName'] == 'Site_3_vEdge_Template_NEW')
device_template_object = api.get_device_template_object(device_template['templateId'])
print(json.dumps(device_template_object, indent=2))