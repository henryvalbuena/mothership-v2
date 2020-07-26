import os
import json
import http.client
from typing import Any, Dict

from src.auth.auth import AUTH0_DOMAIN


def latte_token() -> Dict[str, Any]:
    """Get test token for automated tests"""
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    payload = {
        "client_id": f"{os.environ['LATTE_CLIENT']}",
        "client_secret": f"{os.environ['LATTE_SECRET']}",
        "audience": "latte",
        "grant_type": "client_credentials",
    }
    headers = {
        "Content-Type": "application/json",
    }
    conn.request("POST", "/oauth/token", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))["access_token"]


def project_token() -> Dict[str, Any]:
    """Get test token for automated tests"""
    conn = http.client.HTTPSConnection(AUTH0_DOMAIN)
    payload = {
        "client_id": f"{os.environ['PROJECT_CLIENT']}",
        "client_secret": f"{os.environ['PROJECT_SECRET']}",
        "audience": "project",
        "grant_type": "client_credentials",
    }
    headers = {
        "Content-Type": "application/json",
    }
    conn.request("POST", "/oauth/token", json.dumps(payload), headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))["access_token"]
