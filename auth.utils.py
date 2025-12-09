# auth_utils.py
import requests
from fastapi import HTTPException

SECURITY_SERVICE_URL = "http://35.196.138.189:8001/security/decode"

import requests
from fastapi import HTTPException, Header

def verify_token(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(401, "Missing Authorization header")

    try:
        scheme, token = authorization.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(401, "Invalid auth scheme")
    except:
        raise HTTPException(401, "Invalid Authorization format")

    # Call Security Service with the token
    try:
        resp = requests.post(SECURITY_SERVICE_URL, json={"token": token}, timeout=5)
    except:
        raise HTTPException(503, "Security Service unavailable")

    if resp.status_code != 200:
        raise HTTPException(401, "Invalid token")

    # resp.json() →  { "user_id": 11, "role": "admin" }
    return resp.json()
