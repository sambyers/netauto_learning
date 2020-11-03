

class DeviceConfiguration():
    def __init__(self, session):
        self.session = session

    def get_device_list_by_template_id(self, template_id):
        url = f'{self.session.api_url}/template/device/config/attached/{template_id}'
        r = self.session.get(url)
        return r.json()

    def get_device_templates(self, params: dict = None) -> dict:
        url = f'{self.session.api_url}/template/device'
        r = self.session.get(url, params=params)
        return r.json()

    def get_device_template_id_by_name(self, name: str) -> str:
        device_templates = self.get_device_templates()
        return next(tmpl['templateId'] for tmpl in device_templates['data'] if tmpl['templateName'] == name)

    def get_feature_templates(self, params: dict = None) -> dict:
        url = f'{self.session.api_url}/template/feature'
        r = self.session.get(url, params=params)
        return r.json()

    def get_feature_templates_by_name(self, name: str) -> dict:
        feature_templates = self.get_feature_templates()
        return next(d for d in feature_templates['data'] if d['templateName'] == name)

    def get_feature_templates_by_type(self, type: str) -> list:
        feature_templates = self.get_feature_templates()
        return [d for d in feature_templates['data'] if d['templateType'] == type]

    def get_device_template_object(self, template_id: str) -> dict:
        url = f'{self.session.api_url}/template/device/object/{template_id}'
        r = self.session.get(url)
        return r.json()

    def get_device_feature_templates(self) -> list:
        device_templates = self.get_device_templates()
        device_template_ids = []
        for template in device_templates['data']:
            template_obj = self.get_device_template_object(template['templateId'])
            device_template_ids.append(template_obj)
        return device_template_ids
    
    def get_attached_config(self, deviceid) -> dict:
        params = {'deviceId': deviceid}
        url = f'{self.session.api_url}/template/device/config/attachedconfig'
        r = self.session.get(url, params=params)
        return r.json()

    def update_device_template(self, template_id: str, json: dict) -> dict:
        url = f'{self.session.api_url}/template/device/{template_id}'
        r = self.session.put(url, json=json)
        return r.json()

    def create_device_feature_template(self, json: dict) -> dict:
        url = f'{self.session.api_url}/template/device/feature'
        r = self.session.post(url, json=json)
        return r.json()

    def delete_device_feature_template(self, template_id: str) -> int:
        url = f'{self.session.api_url}/template/device/{template_id}'
        r = self.session.delete(url)
        return r.status_code

    def create_feature_template(self, json: dict = None) -> dict:
        url = f'{self.session.api_url}/template/feature'
        r = self.session.post(url, json=json)
        return r.json()

    def delete_feature_template(self, template_id: str) -> int:
        url = f'{self.session.api_url}/template/feature/{template_id}'
        r = self.session.delete(url)
        return r.status_code

    def get_attached_devices_by_template_id(self, template_id: str) -> dict:
        url = f'{self.session.api_url}/template/device/config/attached/{template_id}'
        r = self.session.get(url)
        return r.json()

    def attach_feature_device_template(self, json: dict = None) -> int:
        url = f'{self.session.api_url}/template/device/config/attachfeature'
        r = self.session.post(url, json=json)
        return r.status_code

    def clone_feature_template(self, template_name, suffix) -> dict:
        feature_template = self.get_feature_templates_by_name(template_name)
        feature_template['templateName'] += suffix
        feature_template['templateDescription'] += suffix
        r = self.create_feature_template(feature_template)
        return r

    def clone_device_feature_template(self, template_name, suffix):
        device_templates = self.get_device_feature_templates()
        device_template = next(d for d in device_templates if d['templateName'] == template_name)
        device_template['templateName'] += suffix
        device_template['templateDescription'] += suffix
        r = self.create_device_feature_template(device_template)
        return r

    def add_feature_template_to_device_feature_template_by_name(self, feature_template_name: str, device_template_name: str) -> int:
        device_template_id = self.get_device_template_id_by_name(device_template_name)
        device_template_obj = self.get_device_template_object(device_template_id)
        feature_template = self.get_feature_templates_by_name(feature_template_name)
        template_reference = {
            "templateId": feature_template['templateId'],
            "templateType": feature_template['templateType']
            }
        device_template_obj['generalTemplates'].append(template_reference)
        return self.update_device_template(device_template_id, device_template_obj)