import hashlib
import urllib
import urllib.parse
from asyncio import Future
from datetime import date, datetime
from typing import Dict, Union

import pytz
from requests_futures.sessions import FuturesSession


class PayfastClient:
    def __init__(
        self,
        *,
        version: str = "v1",
        testing_mode: bool = True,
        merchant_id: int,
        merchant_passphrase: str,
        url: str = "https://api.payfast.co.za",
    ) -> None:
        """
        Create a Payfast Client

        :param version:
        :param testing_mode:
        :param merchant_id:
        :param merchant_passphrase:
        :param url:
        """
        self.version = version
        self.testing_mode = testing_mode
        self.merchant_id = str(merchant_id)
        self.merchant_passphrase = merchant_passphrase
        self.session = FuturesSession()
        self.url = url

        self.headers = {
            "merchant-id": self.merchant_id,
            "version": self.version,
        }

    def _generate_signature(self, payload_dict: dict) -> str:
        """
        Generate the signature salted with the passphrase

        https://developers.payfast.co.za/api#authentication
        :param payload_dict:
        :return: signature
        """
        payload = ""
        payload_dict["passphrase"] = self.merchant_passphrase
        sorted_payload_keys = sorted(payload_dict)
        for key in sorted_payload_keys:
            # Get all the data for PayFast and prepare parameter string
            payload += key + "=" + urllib.parse.quote_plus(str(payload_dict[key])) + "&"
        # After looping through remove the last &
        del payload_dict["passphrase"]
        payload = payload[:-1]
        return hashlib.md5(payload.encode()).hexdigest()

    def _send_get_request(self, *, path: str, params: dict) -> Future:
        """
        Sends a get request, and generates the required headers
        :param path:
        :param params:
        :return:
        """
        if self.testing_mode:
            params["testing"] = "true"

        headers = self._get_headers()
        headers["signature"] = self._generate_signature(headers)
        return self.session.get(f"{self.url}{path}", headers=headers, params=params)

    def _send_put_request(self, *, path: str, params: dict, body: dict) -> Future:
        """
        Sends a put request, and generates the required headers
        :param path:
        :param params:
        :return:
        """
        if self.testing_mode:
            params["testing"] = "true"

        headers = self._get_headers()
        headers["signature"] = self._generate_signature({**headers, **body})
        headers["content-type"] = "application/x-www-form-urlencoded"
        return self.session.put(
            f"{self.url}{path}", headers=headers, params=params, data=body
        )

    def _send_patch_request(self, *, path: str, params: dict, body: dict) -> Future:
        """
        Sends a patch request, and generates the required headers
        :param path:
        :param params:
        :return:
        """
        if self.testing_mode:
            params["testing"] = "true"

        headers = self._get_headers()
        headers["signature"] = self._generate_signature({**headers, **body})
        headers["content-type"] = "application/x-www-form-urlencoded"
        return self.session.patch(
            f"{self.url}{path}", headers=headers, params=params, data=body
        )

    def _get_headers(self) -> dict:
        """
        Generate the required headers:
        - merchant-id
        - version
        - timestamp
        Does not include signature
        :return:
        """
        return {
            "timestamp": str(
                datetime.now(tz=pytz.timezone("Africa/Johannesburg")).isoformat(
                    timespec="seconds"
                )
            ),
            **self.headers,
        }

    def ping(self) -> Future:
        """
        Ping
        Used to check if the API is responding to requests.
        :return: The response
        """
        path = "/ping"
        return self._send_get_request(path=path, params={})

    def fetch_subscription(self, *, token: str) -> Future:
        """
        This is the object representing your subscription.
        You can retrieve it to see the details of your subscription.
        :param token:
        :return: Future: {
            "code": 200,
            "status": "success",
            "data": {
                "response": {
                "token": "a3b3ae55-ab8b-b388-df23-4e6882b86ce0",
                "amount": "1628",
                "cycles": "14",
                "cycles_complete": "9",
                "frequency": "3",
                "status": "1",
                "run_date": "2020-07-04"
                }
            }
        }
        """
        path = f"/subscriptions/{token}/fetch"
        return self._send_get_request(path=path, params={})

    def pause_subscription(self, *, token: str, cycles: int = 1) -> Future:
        """
        Should a subscription be paused the remaining payments (cycles) will remain untouched. The end date of the
        subscription moves on by the number of paused frequency period(s). Effectively the customer gains a payment
        gap and the number of payments will still be the same as originally requested. A free month(s) could be
        provided by pausing (pause) a subscription and reducing the number of cycles by making an update to the
        subscription. :param token: :return:
        """
        path = f"/subscriptions/{token}/pause"
        return self._send_put_request(path=path, params={}, body={"cycles": cycles})

    def unpause_subscription(self, *, token: str) -> Future:
        """
        Unpause a subscription.
        :param token:
        :return:
        """
        path = f"/subscriptions/{token}/unpause"
        return self._send_put_request(path=path, params={}, body={})

    def cancel_subscription(self, *, token: str) -> Future:
        """
        This will cancel a subscription entirely.
        When a subscription is cancelled the customer will be notified of this via email.
        :param token:
        :return:
        """
        path = f"/subscriptions/{token}/cancel"
        return self._send_put_request(path=path, params={}, body={})

    def update_subscription(
        self,
        *,
        token: str,
        cycles: int = None,
        frequency: int = None,
        run_date: date = None,
        amount_in_cents: int = None,
    ) -> Future:
        """
        This allows for multiple subscription values to be updated.
        At least one field must be present
        :param token:
        :param cycles:
        :param frequency:
        :param run_date:
        :param amount_in_cents:
        :return:
        """
        body: Dict[str, Union[str, int]] = {}
        if cycles:
            body["cycles"] = cycles
        if frequency:
            body["frequency"] = frequency
        if amount_in_cents:
            body["amount"] = amount_in_cents
        if run_date:
            body["run_date"] = str(run_date)

        if not body:
            raise ValueError("At least one field must be set in update_subscription.")

        path = f"/subscriptions/{token}/update"
        return self._send_patch_request(path=path, params={}, body={})
