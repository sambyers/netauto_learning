

class DeviceRealtime():
    def __init__(self, session):
        self.session = session

    def get_tunnel_stats(self, device_id: str) -> dict:
        params = {'deviceId': device_id}
        url = f'{self.session.api_url}/device/tunnel/statistics'
        r = self.session.get(url, params=params)
        return r.json()

    def get_control_stats(self, device_id: str) -> dict:
        params = {'deviceId': device_id}
        url = f'{self.session.api_url}/device/control/statistics'
        r = self.session.get(url, params=params)
        return r.json()
