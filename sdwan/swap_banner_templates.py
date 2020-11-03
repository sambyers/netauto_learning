import json
import sys
from yaml import safe_load
from sdwan import Sdwan


# Swap feature template of a device template given the old and new feature template names
# Type hints added to keep track of data types expected
def swap_feature_templates(device_template_obj: dict, feature_templates: dict, old_template_name: str, new_template_name: str) -> dict:
    # Generator expression to grab the only template with the old template name 
    old_template_id = next(d['templateId'] for d in feature_templates['data'] if d['templateName'] == old_template_name)
    # Generator expression to grab the only template with the new template name
    new_template = next(d for d in feature_templates['data'] if d['templateName'] == new_template_name)
    # Find the old template in the device template and replace with new one
    for feature_tmpl in device_template_obj['generalTemplates']:
        if old_template_id == feature_tmpl['templateId']:
            device_template_obj['generalTemplates'].remove(feature_tmpl)
            device_template_obj['generalTemplates'].append(new_template)
    return device_template_obj

config_file = sys.argv[1]
device_template_name = sys.argv[2]
feature_template_old = sys.argv[3]
feature_template_new = sys.argv[4]

with open(config_file) as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)

# Get all feature templates
feature_templates = api.deviceconfiguration.get_feature_templates()

# Get device template ID given a template name
site_device_template_id = api.deviceconfiguration.get_device_template_id_by_name(device_template_name)

# Get the device template object that contains device template to feature template references
site_device_template_obj = api.deviceconfiguration.get_device_template_object(site_device_template_id)

# Swap old feature template for a new one by name
updated_device_template_obj = swap_feature_templates(site_device_template_obj, feature_templates, 'remote_site_banner1', 'remote_site_banner2')

# Update device template with newly swapped feature template
update_result = api.deviceconfiguration.update_device_template(site_device_template_id, updated_device_template_obj)
