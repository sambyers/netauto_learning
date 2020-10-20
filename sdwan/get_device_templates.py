from sdwan import Sdwan
from yaml import safe_load
import json


with open('config.yml') as fh:
    config = safe_load(fh.read())

s = Sdwan(**config, verify_tls=False)
response = s.get_device_templates()
print(json.dumps(response['data'], indent=2))