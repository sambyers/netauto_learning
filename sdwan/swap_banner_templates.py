from sdwan import Sdwan
from yaml import safe_load


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

with open('config.yml') as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)

# Get all feature templates
feature_templates = api.get_feature_templates()

device_templates = api.get_device_templates()
# Generator expression to grab our single device template based on name
site1_device_template = next(d for d in device_templates['data'] if d['templateName'] == 'site1_device_template')
site1_device_template_id = site1_device_template['templateId']

# Get the device template object that contains device template to feature template references
site1_device_template_obj = api.get_device_template_object(site1_device_template_id)

# Swap old feature template for a new one by name
updated_device_template_obj = swap_feature_templates(site1_device_template_obj, feature_templates, 'remote_site_banner2', 'remote_site_banner1')

# Update device template with newly swapped feature template
update_result = api.update_device_template(site1_device_template_id, updated_device_template_obj)
