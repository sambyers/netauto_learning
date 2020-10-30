from sdwan import Sdwan
from yaml import safe_load
import json


with open('config.yml') as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)

banner_template = {
  "templateName": "",
  "templateDescription": "",
  "templateType": "banner",
  "deviceType": [
    "vedge-CSR-1000v"
  ],
  "factoryDefault": False,
  "templateMinVersion": "15.0.0",
  "templateDefinition": {
    "login": {
        "vipObjectType": "object",
        "vipType":"variableName",
        "vipValue":"",
        "vipVariableName": "banner_login"
        },
    "motd": {
        "vipObjectType": "object",
        "vipType": "variableName",
        "vipValue": "",
        "vipVariableName": "banner_motd"
        }
    }
}

for i in range(1, 3):
    name = f'remote_site_banner{i}'
    banner_template['templateName'] = name
    banner_template['templateDescription'] = name
    response = api.deviceconfiguration.create_feature_template(json=banner_template)
    print(json.dumps(response, indent=2))