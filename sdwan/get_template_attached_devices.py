from sdwan import Sdwan
from yaml import safe_load
import json


with open('config.yml') as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)
template_id = api.get_device_template_id_by_name('Site_3_vEdge_Template')
attached_devices = api.get_template_attached_devices(template_id)
print(json.dumps(attached_devices, indent=2))