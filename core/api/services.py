import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def auth():
    return HTTPBasicAuth(settings.KAPITAL_USERNAME, settings.KAPITAL_PASSWORD)


def create_order(order_data):
    url = f"{settings.KAPITAL_BASE_URL}/order/"

    response = requests.post(
        url,
        json={"order": order_data},
        headers=HEADERS,
        auth=auth(),
        timeout=30
    )

    try:
        return response.json()
    except:
        return {
            "error": "Cloudflare block or invalid response",
            "status_code": response.status_code,
            "raw_response": response.text[:500]
        }

def get_order(order_id, password=None, detailed=False):
    url = f"{settings.KAPITAL_BASE_URL}/order/{order_id}"

    params = {}
    if detailed:
        params = {
            "password": password,
            "tranDetailLevel": 2,
            "tokenDetailLevel": 2,
            "orderDetailLevel": 2
        }

    response = requests.get(
        url,
        headers=HEADERS,
        auth=auth(),
        params=params,
        timeout=30
    )

    try:
        return response.json()
    except:
        return {
            "error": "Cloudflare block or invalid response",
            "status_code": response.status_code,
            "raw_response": response.text[:500]
        }