from sdwan import Sdwan
from yaml import safe_load


with open('config.yml') as fh:
    config = safe_load(fh.read())

s = Sdwan(**config, verify_tls=False)
s.logout()