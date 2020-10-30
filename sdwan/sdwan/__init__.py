"""
Minimal SD-WAN SDK for learning purposes only.
"""

import logging
from .session import Session
from .deviceconfiguration import DeviceConfiguration
from .devicestate import DeviceState
from .deviceaction import DeviceAction
from .devicerealtime import DeviceRealtime
from .admin import Admin
from .troubleshooting import Troubleshooting


class Sdwan():
    def __init__(self, vmanage, port, username, password, verify_tls):

        # Setup logging
        log = logging.getLogger(__name__)
        log.setLevel(logging.INFO)
        console = logging.StreamHandler()
        log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console.setFormatter(log_formatter)
        log.addHandler(console)

        self.session = Session(vmanage, port, username, password, verify_tls, logger=log)
        self.deviceconfiguration = DeviceConfiguration(self.session)
        self.devicestate = DeviceState(self.session)
        self.deviceaction = DeviceAction(self.session)
        self.devicerealtime = DeviceRealtime(self.session)
        self.admin = Admin(self.session)
        self.troubleshooting = Troubleshooting(self.session)