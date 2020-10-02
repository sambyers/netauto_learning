from ncclient import manager
from jinja2 import Environment, PackageLoader, select_autoescape
import sys
import yaml


args = cliargs()

rpc = '''<?xml version="1.0" encoding="utf-8"?> 
 <rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="101"> 
   <cisco-ia:save-config xmlns:cisco-ia="http://cisco.com/yang/cisco-ia"/> 
 </rpc>'''

with manager.connect(host=args.host, port=830,
                    username=args.username, password=args.password,
                    device_params={'name':'csr'}) as m:
    rpc_obj = m.rpc(rpc)

