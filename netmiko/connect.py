from netmiko import ConnectHandler
from config import hosts


for host in hosts:
    device = ConnectHandler(**host)
    print(f'Connected to {host["host"]} successful: {device.is_alive()}')
    device.disconnect()