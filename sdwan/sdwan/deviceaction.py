

class DeviceAction():
    def __init__(self, session):
        self.session = session

    def get_device_details(self, device_category: str, params: dict = None) -> dict:
        url = f'{self.session.api_url}/system/device/{device_category}'
        r = self.session.get(url, params=params)
        return r.json()