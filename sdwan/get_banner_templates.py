from sdwan import Sdwan
from yaml import safe_load
import json


with open('config.yml') as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)

# Get all feature templates of type banner
response = api.get_feature_templates()
banner_template = [d for d in response['data'] if d['templateType'] == 'banner']
print(json.dumps(banner_template, indent=2))