from sdwan import Sdwan
from yaml import safe_load
import json


with open('config.yml') as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)

response = api.deviceconfiguration.clone_device_feature_template('Site_3_vEdge_Template', '_CLONED')
print(json.dumps(response))