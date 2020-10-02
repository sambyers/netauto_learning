from netmiko import ConnectHandler
from config import hosts
from random import randrange
import os


def show_ip(device):
    show_ip_cmd = 'show ip int brief | exc unassigned'
    output = device.send_command(show_ip_cmd)
    print(f'Current Assigned IP Interfaces: \n {output}\n')

# Generate random loopback interface number
loopback_int = randrange(1000)
for host in hosts:
    # Generate random loopback interface configuration
    loopback_config = [
        f'interface loopback {loopback_int}',
        f'ip address {randrange(1, 198)}.{randrange(255)}.{randrange(255)}.{randrange(255)} 255.255.255.255',
        'description TERRA FIRMA'
    ]
    # Pass in dictionary as keyword args from hosts.json file and connect to the device
    device = ConnectHandler(**host)
    host = host.get("host")
    print(f'Connected to {host}')
    show_ip(device)
    print('Configuring new Loopback interface...\n')
    filename = f'{host}/loopback.cfg'
    # Make directory for host configuration if it doesn't exist yet
    # If it exists already, do nothing
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    # Save configuration that will be applied in a host directory
    with open(filename, 'w') as fh:
        fh.write('\n'.join(loopback_config))
    # Send command list to device
    cfg_output = device.send_config_set(loopback_config)
    print(cfg_output,'\n')
    show_ip(device)
    print(f'Disconnecting from {host}\n')
    device.disconnect()