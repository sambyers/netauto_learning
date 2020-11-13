import json
import sys
from yaml import safe_load
from sdwan import Sdwan


config_file = sys.argv[1]
with open(config_file) as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)
cert_list = api.deviceaction.get_controller_cert_list()
root_cert = api.deviceaction.get_root_cert()

print(json.dumps(cert_list, indent=2))
print(json.dumps(root_cert, indent=2))