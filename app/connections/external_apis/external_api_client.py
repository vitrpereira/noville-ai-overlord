import requests


class ExternalApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, headers=None):
        response = requests.get(f"{self.base_url}/{endpoint}", headers=headers)
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, data=None, headers=None):
        response = requests.post(
            f"{self.base_url}{endpoint}", data=data, headers=headers
        )
        response.raise_for_status()
        return response.json()
