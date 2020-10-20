from sdwan import Sdwan
from yaml import safe_load
import json


with open('config.yml') as fh:
    config = safe_load(fh.read())

s = Sdwan(**config, verify_tls=False)
params = {'system-ip': '10.10.1.13'}
response = s.get_devices(params=params)
print(json.dumps(response['data'], indent=2))