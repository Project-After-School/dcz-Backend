import jwt
from datetime import datetime, timedelta

SECRET_KEY = "dkssudgktpdywjsmsrlarkdmsdlqslqslekwjsmseoejrthvmxnpd"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 999999

class JWTTokenProvider:
    def generate_token(self, account_id: str, role: str) -> str:
        to_encode = {"sub": account_id, "role": role}
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
