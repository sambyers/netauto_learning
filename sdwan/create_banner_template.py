import json
import sys
from yaml import safe_load
from sdwan import Sdwan


config_file = sys.argv[1]
template_file = sys.argv[2]

with open(config_file) as fh:
    config = safe_load(fh.read())

with open (template_file) as fh:
  template = json.loads(fh.read())

api = Sdwan(**config, verify_tls=False)

for i in range(1, 3):
    name = f'remote_site_banner{i}'
    template['templateName'] = name
    template['templateDescription'] = name
    response = api.deviceconfiguration.create_feature_template(json=template)
    print(json.dumps(response, indent=2))