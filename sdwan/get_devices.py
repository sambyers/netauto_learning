import json
import sys
from yaml import safe_load
from sdwan import Sdwan
from tabulate import tabulate


config_file = sys.argv[1]
with open(config_file) as fh:
    config = safe_load(fh.read())

def create_device_table(response):
    headers = ['Hostname', 'Device Type', 'Device ID', 'System IP', 'Site ID', 'Version', 'Device Model']
    table = []
    for dev in response['data']:
        row = [dev['host-name'], dev['device-type'], dev['deviceId'], dev['system-ip'], dev['site-id'], dev['version'], dev['device-model']]
        table.append(row)
    return table, headers

api = Sdwan(**config, verify_tls=False)
response = api.devicestate.get_devices()
# print(json.dumps(response['data'], indent=2))

device_table, table_headers = create_device_table(response)

print()
print(tabulate(device_table, headers=table_headers))