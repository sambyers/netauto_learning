from sdwan import Sdwan
from yaml import safe_load
import json
import logging

with open('config.yml') as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)

device_templates = api.get_device_templates()
site1_device_template = next(d for d in device_templates['data'] if d['templateName'] == 'site1_device_template')
site1_tmpl_id = site1_device_template['templateId']
site1_tmpl_obj = api.get_device_template_object(site1_tmpl_id)

feature_templates = api.get_feature_templates()
banner_template = next(d for d in feature_templates['data'] if d['templateName'] == 'remote_site_banner1')

banner_template_ref = {
      "templateId": banner_template['templateId'],
      "templateType": banner_template['templateType']
    }

site1_tmpl_obj['generalTemplates'].append(banner_template_ref)

api.update_device_template(site1_tmpl_id, site1_tmpl_obj)

updated_device_template = api.get_device_template_object(site1_tmpl_id)
print(json.dumps(updated_device_template, indent=2))