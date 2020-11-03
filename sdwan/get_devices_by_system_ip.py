import json
import sys
from yaml import safe_load
from sdwan import Sdwan


config_file = sys.argv[1]
with open(config_file) as fh:
    config = safe_load(fh.read())

s = Sdwan(**config, verify_tls=False)
params = {'system-ip': '10.10.1.17'}
response = s.get_devices(params=params)
print(json.dumps(response['data'], indent=2))