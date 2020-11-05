import json
import sys
from yaml import safe_load
from sdwan import Sdwan


config_file = sys.argv[1]
with open(config_file) as fh:
    config = safe_load(fh.read())

api = Sdwan(**config, verify_tls=False)
users = api.admin.get_users()
groups = api.admin.get_usergroups()
# print(json.dumps(response, indent=2))

for user in users.data:
    print(f'Username: {user.userName}')
for group in groups.data:
    print(f'Group name: {group.groupName}')
