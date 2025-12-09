# auth_utils.py
import requests
from fastapi import HTTPException

SECURITY_SERVICE_URL = "http://35.196.138.189:8001/security/decode"

def decode_jwt_from_header(authorization: str):
    # Header must be: "Bearer <token>"
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    token = authorization.split(" ")[1]

    # Call Security Service decode endpoint
    resp = requests.post(f"{SECURITY_SERVICE_URL}?token={token}")

    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return resp.json()   # Expected: {"user_id":..., "uni":..., "role":...}
