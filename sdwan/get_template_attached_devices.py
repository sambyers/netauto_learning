import json
import sys
from yaml import safe_load
from sdwan import Sdwan


config_file = sys.argv[1]
with open(config_file) as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)
template_id = api.deviceconfiguration.get_device_template_id_by_name('Site_3_vEdge_Template')
attached_devices = api.deviceconfiguration.get_template_attached_devices(template_id)
print(json.dumps(attached_devices, indent=2))