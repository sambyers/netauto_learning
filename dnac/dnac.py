import requests


requests.packages.urllib3.disable_warnings()

class DNAC():
    def __init__(self, host: str, username: str, password: str) -> None:
        '''
        Args:
            host: string IP or FQDN of DNAC
            username: string username for DNAC
            password: string password for DNAC
        '''
        self.host = host
        self.username = username
        self.password = password
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.token = None
        self.auth_resp = self.auth()

    def auth(self) -> object:
        path = f'{self.host}/dna/system/api/v1/auth/token'
        resp = requests.post(path, auth=(self.username, self.password), headers=self.headers, verify=False)
        resp.raise_for_status()
        resp_json = resp.json()
        self.token = resp_json.get('Token')
        self.headers['X-Auth-Token'] = self.token
        return resp_json

    def request(self, method: str, path: str, params: dict = None, body: dict = None) -> str:
        method = str(method).lower()
        req = getattr(requests, method)
        resp = req(path, headers=self.headers, verify=False, params=params, json=body)
        resp.raise_for_status()
        return resp.json()

    def get_site_health(self) -> str:
        path = f'{self.host}/dna/intent/api/v1/site-health'
        return self.request('get', path)

    def get_wireless_site_health(self) -> str:
        site_health = self.get_site_health()
        wireless_health = []
        for site in site_health.get('response'):
            wifi = {k:v for k,v in site.items() if 'wireless' in k.lower() or 'siteName' in k}
            wireless_health.append(wifi)
        return wireless_health

    def get_events(self) -> str:
        params = {'tags': 'ASSURANCE'}
        path = f'{self.host}/dna/intent/api/v1/events'
        return self.request('get', path, params=params)
    
    def get_event_subscriptions(self) -> str:
        path = f'{self.host}/dna/intent/api/v1/event/subscription'
        return self.request('get', path)

    def create_event_subscriptions(self, body: dict) -> str:
        '''
        Args:
            body: dict of the subscription to create
        '''
        path = f'{self.host}/dna/intent/api/v1/event/subscription'
        return self.request('post', path, body=body)
    
    def get_event_status(self, subscription_id: str) -> str:
        '''
        Args:
            subscription_id: string the ID of the subscription to get from DNAC
        '''
        path = f'{self.host}/dna/intent/api/v1/event/api-status/{subscription_id}'
        return self.request('get', path)
    
    def delete_event_subscriptions(self, subscription_ids: list) -> str:
        '''
        Args:
            subscription_ids: list of subscription IDs
        '''
        params = {'subscriptions': subscription_ids}
        path = f'{self.host}/dna/intent/api/v1/event/subscription'
        return self.request('delete', path, params=params)

    def get_notifications(self) -> str:
        path = f'{self.host}/dna/intent/api/v1/event/event-series'
        return self.request('get', path)