'''
Minimal Cisco SD-WAN SDK for labbing
'''
import logging
from random import randint
import requests


# Disabling warnings about self assigned certs
requests.packages.urllib3.disable_warnings()

# Setup logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
console = logging.StreamHandler()
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(log_formatter)
log.addHandler(console)

class Sdwan():
    def __init__(self, 
        log: logging.Logger = log,
        vmanage: str = None,
        port: str = None,
        username: str = None,
        password: str = None,
        verify_tls: bool = True) -> None:

        self.log = log
        self.vmanage = vmanage
        self.port = port
        self.vmanage_url = f'https://{self.vmanage}:{self.port}'
        self.api_url = f'https://{self.vmanage}:{self.port}/dataservice'
        self.credentials = {'j_username': username, 'j_password': password}
        self.verify_tls = verify_tls
        self.session = requests.session()
        self.login = self.authenticate() # Login to vManage
        self.token = self.get_token() # Grab token
        self.headers = {'X-XSRF-TOKEN': self.token} # Store token in a dict for use as headers

    def post(self, url: str, headers: dict = None, params: dict = None, data: dict = None, json: dict = None) -> requests.Response:
        self.log.info(f'POST {url}')
        self.log.debug(f'URL: {url}, Headers: {headers}, Params: {params}, Form data: {data}, JSON: {json}')
        r = self.session.post(url, headers=headers, params=params, data=data, json=json, verify=self.verify_tls)
        self.log.info(f'Status Code {r.status_code}')
        self.log.debug('Response:')
        self.log.debug(f'{r.text}')
        r.raise_for_status()
        return r

    def put(self, url: str, headers: dict = None, params: dict = None, data: dict = None, json: dict = None) -> requests.Response:
        self.log.info(f'PUT {url}')
        self.log.debug(f'URL: {url}, Headers: {headers}, Params: {params}, Form data: {data}, JSON: {json}')
        r = self.session.put(url, headers=headers, params=params, data=data, json=json, verify=self.verify_tls)
        self.log.info(f'Status Code {r.status_code}')
        self.log.debug('Response:')
        self.log.debug(f'{r.text}')
        r.raise_for_status()
        return r
    
    def get(self, url: str = None, headers: dict = None, params: dict = None) -> requests.Response:
        self.log.info(f'GET {url}')
        self.log.debug(f'URL: {url}, Headers: {headers}, Params: {params}')
        r = self.session.get(url, headers=headers, params=params, verify=self.verify_tls)
        self.log.info(f'Status Code {r.status_code}')
        self.log.debug('Response:')
        self.log.debug(f'{r.text}')
        r.raise_for_status()
        return r

    def delete(self, url: str, headers: dict = None, params: dict = None, data: dict = None, json: dict = None) -> requests.Response:
        self.log.info(f'DELETE {url}')
        self.log.debug(f'URL: {url}, Headers: {headers}, Params: {params}, Form data: {data}, JSON: {json}')
        r = self.session.delete(url, headers=headers, params=params, data=data, json=json, verify=self.verify_tls)
        self.log.info(f'Status Code {r.status_code}')
        self.log.debug('Response:')
        self.log.debug(f'{r.text}')
        r.raise_for_status()
        return r

    def authenticate(self) -> int:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        url = f'https://{self.vmanage}:{self.port}/j_security_check'
        self.log.info('Authenticating to vManage...')
        r = self.post(url, headers=headers, data=self.credentials)
        return r.status_code

    def get_token(self) -> str:
        url = f'{self.api_url}/client/token'
        self.log.info('Requesting token...')
        r =  self.get(url)
        return r.text

    def logout(self) -> int:
        url = f'/logout?nocache={randint(0, 1000)}'
        self.log.info('Logging out...')
        r = self.get(url)
        return r.status_code

    def get_devices(self, params: dict = None) -> dict:
        url = f'{self.api_url}/device/'
        r = self.get(url, headers=self.headers, params=params)
        return r.json()

    def get_interface_stats(self, params: dict = None) -> dict:
        url = f'{self.api_url}/statistics/interface'
        r = self.get(url, headers=self.headers, params=params)
        return r.json()

    def get_alarms(self, params: dict = None) -> dict:
        url = f'{self.api_url}/alarms'
        r = self.get(url, headers=self.headers, params=params)
        return r.json()

    def get_device_templates(self, params: dict = None) -> dict:
        url = f'{self.api_url}/template/device'
        r = self.get(url, headers=self.headers, params=params)
        return r.json()
    
    def get_device_template_id_by_name(self, name: str) -> str:
        device_templates = self.get_device_templates()
        return next(tmpl['templateId'] for tmpl in device_templates['data'] if tmpl['templateName'] == name)

    def get_feature_templates(self, params: dict = None) -> dict:
        url = f'{self.api_url}/template/feature'
        r = self.get(url, headers=self.headers, params=params)
        return r.json()

    def get_device_template_object(self, template_id: str) -> dict:
        url = f'{self.api_url}/template/device/object/{template_id}'
        r = self.get(url, headers=self.headers)
        return r.json()

    def get_device_feature_templates(self) -> list:
        device_templates = self.get_device_templates()
        device_template_ids = []
        for template in device_templates['data']:
            template_obj = self.get_device_template_object(template['templateId'])
            device_template_ids.append(template_obj)
        return device_template_ids

    def update_device_template(self, template_id: str, json: dict) -> dict:
        url = f'{self.api_url}/template/device/{template_id}'
        r = self.put(url, headers=self.headers, json=json)
        return r.json()

    def create_device_feature_template(self, json: dict) -> dict:
        url = f'{self.api_url}/template/device/feature'
        r = self.post(url, headers=self.headers, json=json)
        return r.json()
        
    def delete_device_feature_template(self, template_id: str) -> int:
        url = f'{self.api_url}/template/device/{template_id}'
        r = self.delete(url, headers=self.headers)
        return r.status_code

    def create_feature_template(self, json: dict = None) -> dict:
        url = f'{self.api_url}/template/feature'
        r = self.post(url, headers=self.headers, json=json)
        return r.json()

    def delete_feature_template(self, template_id: str) -> int:
        url = f'{self.api_url}/template/feature/{template_id}'
        r = self.delete(url, headers=self.headers)
        return r.status_code
    
    def get_template_attached_devices(self, template_id: str) -> dict:
        url = f'{self.api_url}/template/device/config/attached/{template_id}'
        r = self.get(url, headers=self.headers)
        return r.json()

    def attach_feature_device_template(self, json: dict = None) -> int:
        url = f'{self.api_url}/template/device/config/attachfeature'
        r = self.post(url, headers=self.headers, json=json)
        return r.status_code