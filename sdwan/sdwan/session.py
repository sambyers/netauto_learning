import requests


# Disabling warnings about self assigned certs
requests.packages.urllib3.disable_warnings()

class Session():
    def __init__(self,
        vmanage: str = None,
        port: str = None,
        username: str = None,
        password: str = None,
        verify_tls: bool = True,
        logger: object = None) -> None:

        self.log = logger
        self.vmanage = vmanage
        self.port = port
        self.vmanage_url = f'https://{self.vmanage}:{self.port}'
        self.api_url = f'https://{self.vmanage}:{self.port}/dataservice'
        self.credentials = {'j_username': username, 'j_password': password}
        self.verify_tls = verify_tls
        self.session = requests.session()
        self.auth_result = self.authenticate() # Login to vManage
        self.token = self.get_token() # Grab token
        self.headers = {'X-XSRF-TOKEN': self.token} # Store token in a dict for use as headers

    def authenticate(self) -> int:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        url = f'https://{self.vmanage}:{self.port}/j_security_check'
        self.log.info('Authenticating to vManage...')
        r = self.post(url, headers=headers, data=self.credentials)
        return r.status_code

    def get_token(self) -> str:
        headers = {'Content-Type': 'application/json'}
        url = f'{self.api_url}/client/token'
        self.log.info('Requesting token...')
        r =  self.get(url, headers=headers)
        return r.text

    def logout(self) -> int:
        url = f'/logout?nocache={randint(0, 1000)}'
        self.log.info('Logging out...')
        r = self.get(url)
        return r.status_code

    def post(self, url: str, headers: dict = None, params: dict = None, data: dict = None, json: dict = None) -> requests.Response:
        headers = headers or self.headers
        self.log.info(f'POST {url}')
        self.log.debug(f'URL: {url}, Headers: {headers}, Params: {params}, Form data: {data}, JSON: {json}')
        r = self.session.post(url, headers=headers, params=params, data=data, json=json, verify=self.verify_tls)
        self.log.info(f'Status Code {r.status_code}')
        self.log.debug('Response:')
        self.log.debug(f'{r.text}')
        r.raise_for_status()
        return r

    def put(self, url: str, headers: dict = None, params: dict = None, data: dict = None, json: dict = None) -> requests.Response:
        headers = headers or self.headers
        self.log.info(f'PUT {url}')
        self.log.debug(f'URL: {url}, Headers: {headers}, Params: {params}, Form data: {data}, JSON: {json}')
        r = self.session.put(url, headers=headers, params=params, data=data, json=json, verify=self.verify_tls)
        self.log.info(f'Status Code {r.status_code}')
        self.log.debug('Response:')
        self.log.debug(f'{r.text}')
        r.raise_for_status()
        return r
    
    def get(self, url: str = None, headers: dict = None, params: dict = None) -> requests.Response:
        headers = headers or self.headers
        self.log.info(f'GET {url}')
        self.log.debug(f'URL: {url}, Headers: {headers}, Params: {params}')
        r = self.session.get(url, headers=headers, params=params, verify=self.verify_tls)
        self.log.info(f'Status Code {r.status_code}')
        self.log.debug('Response:')
        self.log.debug(f'{r.text}')
        r.raise_for_status()
        return r

    def delete(self, url: str, headers: dict = None, params: dict = None, data: dict = None, json: dict = None) -> requests.Response:
        headers = headers or self.headers
        self.log.info(f'DELETE {url}')
        self.log.debug(f'URL: {url}, Headers: {headers}, Params: {params}, Form data: {data}, JSON: {json}')
        r = self.session.delete(url, headers=headers, params=params, data=data, json=json, verify=self.verify_tls)
        self.log.info(f'Status Code {r.status_code}')
        self.log.debug('Response:')
        self.log.debug(f'{r.text}')
        r.raise_for_status()
        return r