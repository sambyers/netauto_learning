import requests
import time
import logging


requests.packages.urllib3.disable_warnings()

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
console = logging.StreamHandler()
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(log_formatter)
log.addHandler(console)

class TaskPollerTimeout(Exception):
    pass

class DNAC():
    def __init__(self, host: str, username: str, password: str, task_poll_interval: int = 5, task_poll_attempts: int = 6, log: logging.Logger = log) -> None:
        '''
        Args:
            host: string IP or FQDN of DNAC
            username: string username for DNAC
            password: string password for DNAC
        '''
        self.host = host
        self.username = username
        self.password = password
        self.task_poll_interval = task_poll_interval # The length of seconds we wait before we check if DNAC has completed a task.
        self.task_poll_attempts = task_poll_attempts # The count of attempts we make to confirm if DNAC has completed a task.
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.log = log
        self.token = None
        self.auth_resp = self.auth()

    def auth(self) -> object:
        path = f'{self.host}/dna/system/api/v1/auth/token'
        log.info(f'POST {path}')
        resp = requests.post(path, auth=(self.username, self.password), headers=self.headers, verify=False)
        resp.raise_for_status()
        resp_json = resp.json()
        self.token = resp_json.get('Token')
        self.headers['X-Auth-Token'] = self.token
        return resp_json

    def request(self, method: str, path: str, params: dict = None, body: dict = None) -> dict:
        method = str(method).lower()
        req = getattr(requests, method)
        log.info(f'{method.upper()} {path}')
        resp = req(path, headers=self.headers, verify=False, params=params, json=body)
        log.debug(f'Status code: {resp.status_code}')
        log.debug(resp.text)
        resp.raise_for_status()
        return resp.json()

    def is_task(self, resp_json: dict) -> bool:
        if (
                isinstance(resp_json, dict) and 
                isinstance(resp_json.get('response'), dict) and 
                resp_json['response'].get('taskId')
            ):
                return True
        return False

    def task_handler(self, resp_json):
        task_id = resp_json['response'].get('taskId')
        log.info(f'Starting task handler for taskId {task_id}')
        file_id = self.poll_task_by_id(task_id)
        if file_id:
            return get_file_by_id(file_id)
        else:
            log.error('Task poller timeout. The task may still be running.')
            raise SystemExit(TaskPollerTimeout('Task poller timeout.'))

    def poll_task_by_id(self, id):
        interval = self.task_poll_interval
        attempts = self.task_poll_attempts

        while attempts > 0:
            resp = get_task_by_id(id)
            progress = resp['response']['progress']
            if 'fileId' in progress:
                return resp['response']['progress']['fileId']
            attempts -= 1
            time.sleep(interval)

    def get_task_by_id(self, id):
        path = f'{self.host}/dna/intent/api/v1/task/{id}'
        resp = self.request('get', path)
    
    def get_file_by_id(self, id):
        path = f'{self.host}/dna/intent/api/v1/file/{id}'
        resp = self.request('get', path)

    def get_site_health(self) -> dict:
        path = f'{self.host}/dna/intent/api/v1/site-health'
        return self.request('get', path)

    def get_wireless_site_health(self) -> dict:
        site_health = self.get_site_health()
        wireless_health = []
        for site in site_health.get('response'):
            wifi = {k:v for k,v in site.items() if 'wireless' in k.lower() or 'siteName' in k}
            wireless_health.append(wifi)
        return wireless_health

    def get_client_health(self):
        path = f'{self.host}/dna/intent/api/v1/client-health'
        return self.request('get', path)

    def get_events(self) -> dict:
        params = {'tags': 'ASSURANCE'}
        path = f'{self.host}/dna/intent/api/v1/events'
        return self.request('get', path, params=params)
    
    def get_event_subscriptions(self) -> dict:
        path = f'{self.host}/dna/intent/api/v1/event/subscription'
        return self.request('get', path)

    def create_event_subscriptions(self, body: dict) -> dict:
        '''
        Args:
            body: dict of the subscription to create
        '''
        path = f'{self.host}/dna/intent/api/v1/event/subscription'
        return self.request('post', path, body=body)
    
    def get_event_status(self, subscription_id: str) -> dict:
        '''
        Args:
            subscription_id: string the ID of the subscription to get from DNAC
        '''
        path = f'{self.host}/dna/intent/api/v1/event/api-status/{subscription_id}'
        return self.request('get', path)
    
    def delete_event_subscriptions(self, subscription_ids: list) -> dict:
        '''
        Args:
            subscription_ids: list of subscription IDs
        '''
        params = {'subscriptions': subscription_ids}
        path = f'{self.host}/dna/intent/api/v1/event/subscription'
        return self.request('delete', path, params=params)

    def get_notifications(self) -> dict:
        path = f'{self.host}/dna/intent/api/v1/event/event-series'
        return self.request('get', path)

    def get_device_list(self, params: dict = None) -> dict:
        path = f'{self.host}/dna/intent/api/v1/network-device'
        return self.request('get', path, params)
    
    def get_device_summary(self, id):
        path = f'{self.host}/dna/intent/api/v1/network-device/{id}/brief'
        return self.request('get', path)

    def get_device_by_id(self, id):
        path = f'{self.host}/dna/intent/api/v1/network-device/{id}'
        return self.request('get', path)

    def get_command_runner_accepted_cli(self) -> dict:
        path = f'{self.host}/dna/intent/api/v1/network-device-poller/cli/legit-reads'
        return self.request('get', path)

    def create_command_runner(self, body: dict) -> str:
        path = f'{self.host}/dna/intent/api/v1/network-device-poller/cli/read-request'
        resp = self.request('post', path, body=body)
        if self.is_task(resp):
            return self.task_handler(resp)
        return resp

    def get_site(self, params: dict = None) -> dict:
        path = f'{self.host}/dna/intent/api/v1/site'
        return self.request('get', path, params=params)

    def get_site_count(self) -> dict:
        path = f'{self.host}/dna/intent/api/v1/site/count'
        return self.request('get', path)
    
    def get_device_credentials(self, id: str = None) -> dict:
        params = {'siteId': id}
        path = f'{self.host}/dna/intent/api/v1/device-credential'
        return self.request('get', path, params=params)
    
    def get_configuration_templates(self, params: dict = None) -> dict:
        path = f'{self.host}/dna/intent/api/v1/template-programmer/template'
        return self.request('get', path, params=params)
    
    def get_configuration_template_detail(self, id: str) -> dict:
        path = f'{self.host}/dna/intent/api/v1/template-programmer/template/{id}'
        return self.request('get', path)
    
    def get_discoveries_by_range(self, start: int, records: int) -> dict:
        path = f'{self.host}/dna/intent/api/v1/discovery/{start}/{records}'
        return self.request('get', path)