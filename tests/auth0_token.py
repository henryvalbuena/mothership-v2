import os
import json
import http.client
from typing import Any, Dict


def test_token() -> Dict[str, Any]:
    """Get test token for automated tests"""
    conn = http.client.HTTPSConnection("coffe-shop-project.auth0.com")
    payload = {
        "client_id": "198maiZsYJEtoKZyrZ2bYw99uyUmCkfk",
        "client_secret": f"{os.environ['SECRET_TOKEN']}",
        "audience": "drinks",
        "grant_type": "client_credentials",
    }
    headers = {
        "Content-Type": "application/json",
        "Cookie": "did=s%3Av0%3Af45d8260-7bfe-11ea-ade0-2f540a308b4b.nOCHdcqYzCWhtGlimh2qB3eKgv3mBKdywHQunA6bd7M; did_compat=s%3Av0%3Af45d8260-7bfe-11ea-ade0-2f540a308b4b.nOCHdcqYzCWhtGlimh2qB3eKgv3mBKdywHQunA6bd7M",
    }
    conn.request("POST", "/oauth/token", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))
