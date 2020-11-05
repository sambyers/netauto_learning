

class Admin():
    def __init__(self, session):
        self.session = session

    def get_users(self):
        url = f'{self.session.api_url}/admin/user'
        r = self.session.get(url)
        return r.json()

    def create_user(self, json: dict):
        url = f'{self.session.api_url}/admin/user'
        r = self.session.post(url)
        return r.json()

    def delete_user(self, username):
        url = f'{self.session.api_url}/admin/user/{username}'
        r = self.session.delete(url)
        return r.status_code

    def get_usergroups(self):
        url = f'{self.session.api_url}/admin/usergroup'
        r = self.session.get(url)
        return r.json()

    def create_usergroup(self, json: dict):
        url = f'{self.session.api_url}/admin/usergroup'
        r = self.session.post(url, json=json)
        return r.json()