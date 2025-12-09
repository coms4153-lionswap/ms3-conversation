import requests
from fastapi import HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# 定义安全模式，这将使 Swagger UI 出现 "Authorize" 按钮
security = HTTPBearer()

SECURITY_SERVICE_URL = "http://35.196.138.189:8001/security/decode"

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    验证 Token。
    FastAPI 的 HTTPBearer 会自动确保 Header 存在且格式为 "Bearer <token>"。
    credentials.credentials 就是纯 Token 字符串，没有 Bearer 前缀。
    """
    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 调用 Security Service
    try:
        response = requests.post(
            SECURITY_SERVICE_URL, 
            json={"token": token}, 
            timeout=5
        )
    except requests.RequestException:
        # 捕获网络连接、超时等错误
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Security Service unavailable"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 返回用户信息: { "user_id": 11, "role": "admin" }
    return response.json()