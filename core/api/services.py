import requests
import base64
from django.conf import settings


class KapitalService:

    def __init__(self):
        self.base_url = settings.KAPITAL["BASE_URL"]

        credentials = f'{settings.KAPITAL["USERNAME"]}:{settings.KAPITAL["PASSWORD"]}'
        encoded = base64.b64encode(credentials.encode()).decode()

        self.headers = {
            "Authorization": f"Basic {encoded}",
            "Content-Type": "application/json"
        }

    # -----------------------
    # CREATE ORDER (Purchase)
    # -----------------------
    def create_order(self, amount, description="Payment", currency="AZN"):
        url = f"{self.base_url}/order"

        print(self.headers)

        payload = {
            "amount": float(amount),
            "currency": currency,
            "description": description,
            "language": "az",
            "hppRedirectUrl": settings.KAPITAL["CALLBACK_URL"],
            "typeRid": "Order_SMS",
            "hppCofCapturePurposes": [
                "Cit"
            ]
        }

        r = requests.post(url, json=payload, headers=self.headers)
        r.raise_for_status()
        return r.json()

    # -----------------------
    # ORDER DETAILS
    # -----------------------
    def get_order(self, order_id):
        url = f"{self.base_url}/order/{order_id}"
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        return r.json()

    # -----------------------
    # DETAILED ORDER
    # -----------------------
    def get_order_detailed(self, order_id):
        url = (
            f"{self.base_url}/order/{order_id}"
            "?tranDetailLevel=2&tokenDetailLevel=2&orderDetailLevel=2"
        )
        r = requests.get(url, headers=self.headers)
        r.raise_for_status()
        return r.json()

    # -----------------------
    # REDIRECT URL
    # -----------------------
    @staticmethod
    def build_redirect_url(hpp_url, order_id, password):
        return f"{hpp_url}/flex?id={order_id}&password={password}"
