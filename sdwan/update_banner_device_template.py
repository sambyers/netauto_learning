import json
import sys
from yaml import safe_load
from sdwan import Sdwan


config_file = sys.argv[1]
device_template_name = sys.argv[2]
feature_template_name = sys.argv[3]

with open(config_file) as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)

# Add the feature template to the device template
response = api.deviceconfiguration.add_feature_template_to_device_feature_template_by_name(feature_template_name, device_template_name)
# Get device template ID
template_id = api.deviceconfiguration.get_device_template_id_by_name(device_template_name)
# Get device template object that has all feature template references
updated_device_template = api.deviceconfiguration.get_device_template_object(template_id)
# Print results
print(json.dumps(updated_device_template, indent=2))