import requests
import abc


class ExternalApiClient:
    """"
    Parent class for all External APIs handling.
    """

    @classmethod
    def get(cls, endpoint, headers=None):
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return response.json()


    @classmethod
    def post(cls, endpoint, data=None, headers=None):
        response = requests.post(endpoint, data=data, headers=headers)
        response.raise_for_status()
        return response.json()
