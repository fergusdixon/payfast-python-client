# payfast-python-client

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0a0a2acf5df045ceb533c8ee953d23a2)](https://app.codacy.com/gh/fergusdixon/payfast-python-client?utm_source=github.com&utm_medium=referral&utm_content=fergusdixon/payfast-python-client&utm_campaign=Badge_Grade)

Asynchronous Python Client for the [Payfast API](https://developers.payfast.co.za/api)

Uses [requests-futures](https://github.com/ross/requests-futures)

## Installation
Available on [PyPi](https://pypi.org/project/payfast-client/)
```shell
pip install payfast-client
```

## Usage
 ```python
from payfast_client import PayfastClient
client = PayfastClient(merchant_id=123, merchant_passphrase="passphrase")
subscription = client.fetch_subscription(token="abc")
print(subscription)
```
```
<Future at 0x107d88520 state=finished returned Response>
```
```python
print(subscription.result())
```
```
<Response [200]>
```

## Features
- [x] Signature Generation
- [ ] Error Handling (Sometimes errors returned with response_code=200)
- Endpoints
    - [x] GET /ping
    - Recurring Billing
        - [x] GET   /subscriptions/:token/fetch
        - [x] PUT   /subscriptions/:token/pause
        - [x] PUT   /subscriptions/:token/unpause
        - [x] PUT   /subscriptions/:token/cancel
        - [x] PATCH /subscriptions/:token/update
        - [ ] POST  /subscriptions/:token/adhoc
    - Transaction History
        - [ ] GET   /transactions/history
        - [ ] GET   /transactions/history/daily
        - [ ] GET   /transactions/history/weekly
        - [ ] GET   /transactions/history/monthly
    - Credit card transaction query
        - [ ] GET   /process/query/:id
