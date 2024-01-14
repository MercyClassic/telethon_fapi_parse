import os

from api_client import APIClient


def get_api_client() -> APIClient:
    return APIClient(os.environ['api_url'])
