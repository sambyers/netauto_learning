from dnac import DNAC
import json


with open('host.json', 'r') as f:
    host = json.loads(f.read())

dnac = DNAC(**host)

templates = dnac.get_configuration_templates()
# Grab first template ID
id = templates[0].get('templateId')

data = dnac.get_configuration_template_detail(id)
print(json.dumps(data, indent=2))