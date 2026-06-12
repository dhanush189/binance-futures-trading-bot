import hashlib
import hmac
import os
import time
from urllib.parse import urlencode

import requests
from dotenv import load_dotenv

from bot.logging_config import setup_logger

load_dotenv()
logger = setup_logger()

BASE_URL = "https://testnet.binance.vision"

class FuturesClient:
    """
    Thin wrapper around Binance Futures Testnet REST API.
    Handles authentication (HMAC-SHA256 signing) and request execution.
    """

    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")

        if not self.api_key or not self.api_secret:
            raise EnvironmentError(
                "BINANCE_API_KEY and BINANCE_API_SECRET must be set in your .env file."
            )

        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded",
        })

    def _sign(self, params: dict) -> dict:
        """Add timestamp and HMAC-SHA256 signature to request params."""
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def get(self, endpoint: str, params: dict = None) -> dict:
        """Send a signed GET request."""
        params = self._sign(params or {})
        url = BASE_URL + endpoint
        logger.debug(f"GET {url} | params: {params}")

        response = self.session.get(url, params=params, timeout=10)
        return self._handle_response(response)

    def post(self, endpoint: str, params: dict = None) -> dict:
        """Send a signed POST request."""
        params = self._sign(params or {})
        url = BASE_URL + endpoint
        logger.debug(f"POST {url} | params: {params}")

        response = self.session.post(url, data=params, timeout=10)
        return self._handle_response(response)

    def delete(self, endpoint: str, params: dict = None) -> dict:
        """Send a signed DELETE request."""
        params = self._sign(params or {})
        url = BASE_URL + endpoint
        logger.debug(f"DELETE {url} | params: {params}")

        response = self.session.delete(url, params=params, timeout=10)
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> dict:
        """Parse response and raise on API errors."""
        logger.debug(f"Response [{response.status_code}]: {response.text[:500]}")

        try:
            data = response.json()
        except Exception:
            raise ValueError(f"Non-JSON response from API: {response.text}")

        if isinstance(data, dict) and "code" in data and data["code"] != 200:
            raise BinanceAPIError(data.get("code"), data.get("msg", "Unknown error"))

        return data

    def ping(self) -> bool:
        """Check connectivity to Futures Testnet."""
        try:
            url = BASE_URL + "/fapi/v1/ping"
            response = self.session.get(url, timeout=10)
            return response.status_code == 200
        except requests.RequestException:
            return False


class BinanceAPIError(Exception):
    """Raised when Binance API returns an error response."""

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f"APIError(code={code}): {message}")
