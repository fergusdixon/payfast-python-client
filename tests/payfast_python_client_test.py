"""Test for endpoints in the payfast-python-client."""

from asyncio import Future
from datetime import date
from unittest.mock import MagicMock

import pytest
from freezegun import freeze_time

from payfast_client import PayfastClient, __version__

TIME_STR = "2021-03-11T13:34:01+02:00"


@pytest.fixture(autouse=True)
def client() -> PayfastClient:
    """
    Create a test client.

    :return:
    """
    return PayfastClient(
        url="test_api", merchant_id=1, merchant_passphrase="passphrase"
    )


@freeze_time(TIME_STR)
def test_payfast_ping(client: PayfastClient):
    """
    Test the /ping endpoint.

    :param client:
    :return:
    """
    client.session.get = MagicMock(return_value=Future())
    client.ping()
    client.session.get.assert_called_once_with(
        "test_api/ping",
        headers={
            "timestamp": TIME_STR,
            "merchant-id": "1",
            "version": "v1",
            "signature": "12711773d9990e88ba1844a07b4a39f8",
        },
        params={"testing": "true"},
    )


@freeze_time(TIME_STR)
def test_payfast_fetch_subscription(client: PayfastClient):
    """
    Test the fetch subscription endpoint.

    :param client:
    :return:
    """
    client.session.get = MagicMock(return_value=Future())
    token = "123"
    client.fetch_subscription(token=token)
    client.session.get.assert_called_once_with(
        f"test_api/subscriptions/{token}/fetch",
        headers={
            "timestamp": TIME_STR,
            "merchant-id": "1",
            "version": "v1",
            "signature": "12711773d9990e88ba1844a07b4a39f8",
        },
        params={"testing": "true"},
    )


@freeze_time(TIME_STR)
def test_payfast_pause_subscription(client: PayfastClient):
    """
    Test the pause subscription endpoint.

    :param client:
    :return:
    """
    client.session.put = MagicMock(return_value=Future())
    token = "123"
    client.pause_subscription(token=token, cycles=5)
    client.session.put.assert_called_once_with(
        f"test_api/subscriptions/{token}/pause",
        headers={
            "timestamp": TIME_STR,
            "merchant-id": "1",
            "version": "v1",
            "signature": "310d2121102b7b9b6c611fdaab094207",
            "content-type": "application/x-www-form-urlencoded",
        },
        params={"testing": "true"},
        data={"cycles": 5},
    )


@freeze_time(TIME_STR)
def test_payfast_unpause_subscription(client: PayfastClient):
    """
    Test the unpause subscription endpoint.

    :param client:
    :return:
    """
    client.session.put = MagicMock(return_value=Future())
    token = "123"
    client.unpause_subscription(token=token)
    client.session.put.assert_called_once_with(
        f"test_api/subscriptions/{token}/unpause",
        headers={
            "timestamp": TIME_STR,
            "merchant-id": "1",
            "version": "v1",
            "signature": "12711773d9990e88ba1844a07b4a39f8",
            "content-type": "application/x-www-form-urlencoded",
        },
        params={"testing": "true"},
        data={},
    )


@freeze_time(TIME_STR)
def test_payfast_cancel_subscription(client: PayfastClient):
    """
    Test the cancel subscription endpoint.

    :param client:
    :return:
    """
    client.session.put = MagicMock(return_value=Future())
    token = "123"
    client.cancel_subscription(token=token)
    client.session.put.assert_called_once_with(
        f"test_api/subscriptions/{token}/cancel",
        headers={
            "timestamp": TIME_STR,
            "merchant-id": "1",
            "version": "v1",
            "signature": "12711773d9990e88ba1844a07b4a39f8",
            "content-type": "application/x-www-form-urlencoded",
        },
        params={"testing": "true"},
        data={},
    )


@freeze_time(TIME_STR)
def test_payfast_update_subscription(client: PayfastClient):
    """
    Test the update subscription endpoint.

    :param client:
    :return:
    """
    client.session.patch = MagicMock(return_value=Future())
    token = "123"
    client.update_subscription(
        token=token,
        cycles=2,
        frequency=5,
        amount_in_cents=100,
        run_date=date.today(),
    )
    client.session.patch.assert_called_once_with(
        f"test_api/subscriptions/{token}/update",
        headers={
            "timestamp": TIME_STR,
            "merchant-id": "1",
            "version": "v1",
            "signature": "c0542f2e5749f1dc393956c077742b18",
            "content-type": "application/x-www-form-urlencoded",
        },
        params={"testing": "true"},
        data={"cycles": 2, "frequency": 5, "amount": 100, "run_date": "2021-03-11"},
    )


def test_payfast_update_subscription_no_body_fails(client: PayfastClient):
    """
    Test the update subscription endpoint call fails with no fields to update.

    :param client:
    :return:
    """
    client.session.patch = MagicMock(return_value=Future())
    with pytest.raises(ValueError) as error:
        token = "123"
        client.update_subscription(
            token=token,
        )
    assert "At least one field must be set in update_subscription." == str(error.value)
