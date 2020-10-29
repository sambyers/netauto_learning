from sdwan import Sdwan
from yaml import safe_load
import json


with open('config.yml') as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)

site3_template = {
  "templateName": "Site_3_vEdge_Template_NEW",
  "templateDescription": "Site_3_vEdge_Template_NEW",
  "deviceType": "vedge-cloud",
  "factoryDefault": False,
  "configType": "template",
  "policyId": "",
  "featureTemplateUidRange": [],
  "generalTemplates": [
    {
      "templateId": "3166f51a-a9b5-437e-a60a-6cd77cb23c85",
      "templateType": "aaa"
    },
    {
      "templateId": "04893423-8372-4f6c-94a8-fcfe8f42836f",
      "templateType": "bfd-vedge"
    },
    {
      "templateId": "0a411c7f-1e51-4b80-b6eb-d18813ee52b7",
      "templateType": "omp-vedge"
    },
    {
      "templateId": "0df323c1-d05d-47ed-a45c-ab727ebc3cd9",
      "templateType": "security-vedge"
    },
    {
      "templateId": "5c4670e4-3ec0-4b0d-9951-59c3f2a62820",
      "templateType": "system-vedge",
      "subTemplates": [
        {
          "templateId": "7a486387-1623-4d74-8c99-7c1379ee00c5",
          "templateType": "logging"
        }
      ]
    },
    {
      "templateId": "ca019d8e-944f-44c2-9de4-7f4f00c0ba4f",
      "templateType": "vpn-vedge",
      "subTemplates": [
        {
          "templateId": "b4a87e70-39f5-4377-8473-e5b31c51064e",
          "templateType": "vpn-vedge-interface"
        },
        {
          "templateId": "c0a90dc2-6a0b-4f9f-ac26-b3581eb52ac2",
          "templateType": "vpn-vedge-interface"
        }
      ]
    },
    {
      "templateId": "7f376920-7c78-40f7-95df-aa7c9bcbb4a7",
      "templateType": "vpn-vedge",
      "subTemplates": [
        {
          "templateId": "93325f57-0630-46b3-9c50-c603786dcf75",
          "templateType": "vpn-vedge-interface"
        }
      ]
    },
    {
      "templateId": "c3ec5bb2-f682-46ca-93f2-01206c7baba2",
      "templateType": "vpn-vedge",
      "subTemplates": [
        {
          "templateId": "89a022eb-9c5c-4fcd-8c22-056ce25bf7df",
          "templateType": "vpn-vedge-interface"
        }
      ]
    }
  ]
}

response = api.create_device_feature_template(site3_template)
print(json.dumps(response))