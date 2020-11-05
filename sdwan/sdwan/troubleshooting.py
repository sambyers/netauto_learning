

class Troubleshooting():
    def __init__(self, session):
        self.session = session

    def get_devicebringup(self, uuid: str) -> dict:
        params = {'uuid': uuid}
        url = f'{self.session.api_url}/troubleshooting/devicebringup'
        r = self.session.get(url, params=params)
        return r.json()

    def ping(self, deviceip: str) -> dict:
        url = f'{self.session.api_url}/device/tools/ping/{deviceip}'
        r = self.session.post(url)
        return r.json()

