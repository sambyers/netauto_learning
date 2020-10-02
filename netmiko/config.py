# Configuration file
import json


with open('hosts.json', 'r') as f:
    hosts = json.loads(f.read())
