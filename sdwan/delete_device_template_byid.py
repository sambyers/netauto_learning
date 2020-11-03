import json
import sys
from yaml import safe_load
from sdwan import Sdwan


config_file = sys.argv[1]
templateid = sys.argv[2]

with open(config_file) as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)
response = api.deviceconfiguration.delete_device_feature_template(templateid)
print(f'Status code {response}')