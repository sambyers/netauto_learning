from sdwan import Sdwan
from yaml import safe_load
import json


with open('config.yml') as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)

site1_template = {
  "templateName": "site1_device_template",
  "templateDescription": "site1_device_template",
  "deviceType": "vedge-CSR-1000v",
  "configType": "template",
  "factoryDefault": False,
  "policyId": "",
  "featureTemplateUidRange": [],
  "connectionPreferenceRequired": True,
  "connectionPreference": True,
  "generalTemplates": [
    {
      "templateId": "04893423-8372-4f6c-94a8-fcfe8f42836f",
      "templateType": "bfd-vedge"
    },
    {
      "templateId": "5c64dac5-2c0e-4ea3-9ce1-e2727307f532",
      "templateType": "cedge_aaa"
    },
    {
      "templateId": "a782bdf1-9fd1-42ef-9ab7-d220d266c956",
      "templateType": "omp-vedge"
    },
    {
      "templateId": "0df323c1-d05d-47ed-a45c-ab727ebc3cd9",
      "templateType": "security-vedge"
    },
    {
      "templateId": "a4e559d7-d022-45f0-a043-0b75823fee73",
      "templateType": "system-vedge",
      "subTemplates": [
        {
          "templateId": "7a486387-1623-4d74-8c99-7c1379ee00c5",
          "templateType": "logging"
        }
      ]
    },
    {
      "templateId": "0bb15df7-657e-421c-9d2a-9f59f2c17022",
      "templateType": "vpn-vedge",
      "subTemplates": [
        {
          "templateId": "0a110933-fd97-4274-9a7c-d77d626fc3fd",
          "templateType": "vpn-vedge-interface"
        }
      ]
    },
    {
      "templateId": "55f317d9-084e-45e2-88b3-997eb0744db7",
      "templateType": "vpn-vedge"
    }
  ]
}

response = api.create_device_feature_template(site1_template)
print(json.dumps(response))