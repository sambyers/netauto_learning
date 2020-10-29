import json
from sdwan import Sdwan
from yaml import safe_load



with open('config.yml') as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)
response = api.get_feature_templates()
device_template = next(d for d in response['data'] if d['templateName'] == 'remote_site_banner1')
template_id = device_template['templateId']
cloned_name = f"{device_template['templateName']}_CLONED"
cloned_desc = f"{device_template['templateDescription']}_CLONED"
params = {
    'id': template_id,
    'name': cloned_name,
    'desc': cloned_desc
}
cloned_template_id = api.clone_feature_template(params=params)
print(json.dumps(cloned_template_id, indent=2))