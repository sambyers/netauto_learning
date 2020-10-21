from sdwan import Sdwan
from yaml import safe_load
import json


with open('config.yml') as fh:
    config = safe_load(fh.read())

s = Sdwan(**config, verify_tls=False)

response = s.get_device_templates()
print(json.dumps(response['data'], indent=2))

# response = s.get_feature_templates()
# print(json.dumps(response['data'], indent=2))

response = s.get_device_template_object("fb63ce6d-734c-4e5d-9165-e771f1338720")
print(json.dumps(response, indent=2))