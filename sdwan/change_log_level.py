from sdwan import Sdwan
from yaml import safe_load
import json
import logging


with open('config.yml') as fh:
    config = safe_load(fh.read())

s = Sdwan(**config, verify_tls=False)
s.log.setLevel(logging.DEBUG)
s.logout()