import json
import sys
from yaml import safe_load
from sdwan import Sdwan


config_file = sys.argv[1]
with open(config_file) as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)
devices = api.devicestate.get_devices()
device_uuids= [device['uuid'] for device in devices['data'] if device['device-type'] == 'vedge']

device_bringups = {}
ping_results = []
tunnel_stats = {}
control_stats = {}
device_troubleshooting = {}

for device in devices['data']:
    uuid = device['uuid']
    id = device['deviceId']
    device_troubleshooting[id] = {}
    device_troubleshooting[id].update({'bringup': api.troubleshooting.get_devicebringup(uuid)['data']})
    # ping_results.append(api.troubleshooting.ping(device['system-ip']))
    device_troubleshooting[id].update({'tunnelstats': api.devicerealtime.get_tunnel_stats(id)['data']})
    device_troubleshooting[id].update({'controlstats': api.devicerealtime.get_control_stats(id)['data']})


print(json.dumps(device_troubleshooting, indent=2))
