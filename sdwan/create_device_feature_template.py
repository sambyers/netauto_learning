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
response = api.deviceconfiguration.add_device_feature_template(template)
print(json.dumps(response))