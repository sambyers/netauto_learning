from ncclient import manager
from jinja2 import Environment, PackageLoader, select_autoescape
import sys
import yaml


args = cliargs()

with open(args.vars) as fh:
    var_data = yaml.load(fh.read(), Loader=yaml.Loader)

env = Environment(
    loader=PackageLoader('set_mdt_subscription', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('delete_mdt_rpc.xml')
rpc = template.render(
    sub_id=var_data.get('sub_id'),
    source_ip=args.host,
    period=var_data.get('period'),
    xpath=var_data.get('xpath'),
    receiver_ip=var_data.get('receiver_ip'),
    receiver_port=var_data.get('receiver_port')
    )

with manager.connect(host=args.host, port=830,
                    username=args.username, password=args.password,
                    device_params={'name':'csr'}) as m:
    rpc_obj = m.edit_config(target='running', config=rpc)