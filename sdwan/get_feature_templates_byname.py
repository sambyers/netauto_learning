import json
import sys
from yaml import safe_load
from sdwan import Sdwan


config_file = sys.argv[1]
template_name = sys.argv[2]

with open(config_file) as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)
resp = api.deviceconfiguration.get_feature_templates_by_name(template_name)
print(json.dumps(resp, indent=2))