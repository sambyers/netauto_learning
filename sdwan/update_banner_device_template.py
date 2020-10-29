from sdwan import Sdwan
from yaml import safe_load
import json
import logging


with open('config.yml') as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)
response = api.add_feature_template_to_device_feature_template_by_name('remote_site_banner1', 'Site_3_vEdge_Template_CLONED')
template_id = api.get_device_template_id_by_name('Site_3_vEdge_Template_CLONED')
updated_device_template = api.get_device_template_object(template_id)
print(json.dumps(updated_device_template, indent=2))