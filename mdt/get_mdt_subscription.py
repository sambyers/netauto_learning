from json import dumps
from ncclient import manager
from utils import cliargs
import sys
import xmltodict


args = cliargs()

with manager.connect(host=args.host, port=830,
                    username=args.username, password=args.password,
                    device_params={'name':'csr'}) as m:
    config = m.get_config(source='running', filter=('xpath', 'mdt-config-data/mdt-subscription')).data_xml
    oper = m.get(filter=('xpath', 'mdt-oper-data')).data_xml

config_dict = xmltodict.parse(config)
oper_dict = xmltodict.parse(oper)
mdt_config_data = config_dict['data']['mdt-config-data']
mdt_oper_data = oper_dict['data']['mdt-oper-data']
print('\n### MDT Configuration ###')
print(dumps(mdt_config_data, indent=2))
print('\n### MDT Operating Status ###')
print(dumps(mdt_oper_data, indent=2))