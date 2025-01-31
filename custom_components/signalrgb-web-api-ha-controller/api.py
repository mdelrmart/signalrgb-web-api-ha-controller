import requests

class SignalRGBAPI:
    def __init__(self, host, port, username, password):
        self.base_url = f"http://{host}:{port}/effect/apply"
        self.auth = {"username": username, "password": password}

    def set_effect(self, effect_name, **kwargs):
        params = {**self.auth, **kwargs}
        url = f"{self.base_url}/{effect_name.replace(' ', '%20')}"
        response = requests.get(url, params=params)
        return response.status_code == 200
