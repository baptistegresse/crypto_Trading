from dotenv import load_dotenv
import os
import time
import hmac
from urllib.parse import urlencode
import base64
import requests


# Load environment variables from .env file
load_dotenv()


class BitgetClient:
    def __init__(self):
        self.DOMAIN = "	https://api.bitget.com"

    def _get_headers(self, method, request_path, body):
        timestamp = self._get_access_timestamp()

        return {
            "ACCESS-KEY": os.getenv("API_KEY_BITGET"),
            "ACCESS-PASSPHRASE": os.getenv("PASSPHRASE_BITGET"),
            "ACCESS-SIGN": self._get_access_sign(method, request_path, body, timestamp),
            "ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json",
            "locale": "en",
        }

    def _get_access_timestamp(self):
        return str(int(time.time_ns() / 1000000))

    def _get_access_sign(self, method, request_path, body, timestamp):
        return self._sign(
            self._pre_hash(timestamp, method, request_path, str(body)),
            os.getenv("API_KEY_BITGET"),
        )

    def _sign(self, message, secret_key):
        mac = hmac.new(
            bytes(secret_key, encoding="utf8"),
            bytes(message, encoding="utf-8"),
            digestmod="sha256",
        )
        d = mac.digest()

        return base64.b64encode(d)

    def _parse_params_to_str(self, params):
        params = [(key, val) for key, val in params.items()]
        params.sort(key=lambda x: x[0])

        url = "?" + urlencode(params)
        if url == "?":
            return ""
        return url

    def _pre_hash(self, timestamp, method, request_path, body):
        return str(timestamp) + str.upper(method) + request_path + body

    def get(self, url, params={}):
        headers = self._get_headers(
            "GET",
            url,
            {},
        )
        response = requests.get(
            url=f"{self.DOMAIN}{url}", params=params, headers=headers
        )

        return response.json()
