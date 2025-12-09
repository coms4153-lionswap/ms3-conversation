from fastapi import Header, HTTPException
from jose import jwt, JWTError

SECRET_KEY = "LION_SWAP_GOAT_IS_THE_KEY"       # ⚠️ 必须和 Security MS 完全一样
ALGO = "HS256"

def verify_token(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(401, "Missing Authorization header")

    try:
        scheme, token = authorization.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(401, "Invalid auth scheme")
    except:
        raise HTTPException(401, "Invalid Authorization format. Expect: Bearer <token>")

    # Decode JWT
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        return payload   # 传回 token 里面的 user info
    except JWTError:
        raise HTTPException(401, "Invalid or expired JWT")
