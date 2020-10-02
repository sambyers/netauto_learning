from netmiko import ConnectHandler
from config import hosts


def show_ip(device):
    show_ip_cmd = 'show ip int brief | exc unassigned'
    output = device.send_command(show_ip_cmd)
    print(f'Current Assigned IP Interfaces: \n {output}\n')

loopback_config = ['']
for host in hosts:
    # Pass in dictionary as keyword args from hosts.json file and connect to the device
    device = ConnectHandler(**host)
    host = host.get("host")
    print(f'Connected to {host}')
    show_ip(device)
    print('Removing Loopback interface...\n')
    # Open and read configuration from file for a host
    with open(f'{host}/loopback.cfg', 'r') as fh:
        loopback_config = fh.read()
    # Split the string config into a list
    loopback_config = loopback_config.split('\n')
    # Add no in front of all commands in list
    for i in range(len(loopback_config)):
        loopback_config[i] = f'no {loopback_config[i]}'
    # Send command list to device
    cfg_output = device.send_config_set(loopback_config)
    print(cfg_output,'\n')
    show_ip(device)
    print(f'Disconnecting from {host}\n')
    device.disconnect()