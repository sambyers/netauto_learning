

class DeviceState():
    def __init__(self, session):
        self.session = session
    
    def get_devices(self, params: dict = None) -> dict:
        url = f'{self.session.api_url}/device/'
        r = self.session.get(url, params=params)
        return r.json()
    
    def get_interface_stats(self, params: dict = None) -> dict:
        url = f'{self.session.api_url}/statistics/interface'
        r = self.session.get(url, params=params)
        return r.json()

    def get_alarms(self, params: dict = None) -> dict:
        url = f'{self.session.api_url}/alarms'
        r = self.session.get(url, params=params)
        return r.json()

    def get_device_status(self) -> dict:
        url = f'{self.session.api_url}/device/status'
        r = self.session.get(url)
        return r.json()

    def get_vedge_inventory_detail(self) -> dict:
        url = f'{self.session.api_url}/device/vedgeinventory/detail'
        r = self.session.get(url)
        return r.json()

    def get_vedge_inventory_summary(self) -> dict:
        url = f'{self.session.api_url}/device/vedgeinventory/summary'
        r = self.session.get(url)
        return r.json()

    def get_vmanage_systemip(self) -> dict:
        url = f'{self.session.api_url}/device/vmanage'
        r = self.session.get(url)
        return r.json()
