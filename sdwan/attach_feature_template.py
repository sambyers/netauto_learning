import json
import sys
from yaml import safe_load
from sdwan import Sdwan


def fill_device_vars(
    template_id, 
    device_id,
    banner,
    device_ip, 
    host_name,
    vpn_1_ifname,
    vpn_1_ip,
    vpn_512_default_nexthop,
    vpn_512_ifname,
    vpn_512_ip,
    vpn_0_mpls_default_nexthop,
    vpn_0_inet_default_nexthop,
    vpn_0_inet_ifname,
    vpn_0_inet_ip,
    vpn_0_mpls_ifname,
    vpn_0_mpls_ip,
    latitude,
    longitude,
    system_ip,
    site_id
    ):

    filled = {
    "deviceTemplateList": [
        {
        "templateId": template_id,
        "device": [
            {
            "csv-status": "complete",
            "//banner/login": banner,
            "//banner/motd": banner,
            "csv-deviceId": device_id,
            "csv-deviceIP": device_ip,
            "csv-host-name": host_name,
            "/1/vpn_1_if_name/interface/if-name": vpn_1_ifname,
            "/1/vpn_1_if_name/interface/ip/address": vpn_1_ip,
            "/512/vpn-instance/ip/route/0.0.0.0/0/next-hop/vpn_512_next_hop_ip_address/address": vpn_512_default_nexthop,
            "/512/vpn_512_if_name/interface/if-name": vpn_512_ifname,
            "/512/vpn_512_if_name/interface/ip/address": vpn_512_ip,
            "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/mpls_next_hop/address": vpn_0_mpls_default_nexthop,
            "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/public_internet_next_hop/address": vpn_0_inet_default_nexthop,
            "/0/vpn_public_internet_interface/interface/if-name": vpn_0_inet_ifname,
            "/0/vpn_public_internet_interface/interface/ip/address": vpn_0_inet_ip,
            "/0/vpn_mpls_interface/interface/if-name": vpn_0_mpls_ifname,
            "/0/vpn_mpls_interface/interface/ip/address": vpn_0_mpls_ip,
            "//system/host-name": host_name,
            "//system/gps-location/latitude": latitude,
            "//system/gps-location/longitude": longitude,
            "//system/system-ip": system_ip,
            "//system/site-id": site_id,
            "csv-templateId": template_id,
            "selected": "true"
            }
        ],
        "isEdited": False,
        "isMasterEdited": False
        }
    ]
    }
    return filled

config_file = sys.argv[1]
template_id = sys.argv[2]
tempate_vars_file = sys.argv[3]

with open(config_file) as fh:
    config = safe_load(fh.read())

with open(tempate_vars_file) as fh:
    vars = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)

device_template_list = fill_device_vars(template_id, **vars)
print(json.dumps(device_template_list, indent=2))
api.deviceconfiguration.attach_feature_device_template(json=device_template_list)
device_config = api.deviceconfiguration.get_attached_config(vars['device_id'])
print(json.dumps(device_config, indent=2))