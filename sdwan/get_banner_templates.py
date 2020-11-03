import json
import sys
from yaml import safe_load
from sdwan import Sdwan


config_file = sys.argv[1]
with open(config_file) as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)

# Get all feature templates of type banner
response = api.deviceconfiguration.get_feature_templates()
banner_template = [d for d in response['data'] if d['templateType'] == 'banner']
print(json.dumps(banner_template, indent=2))