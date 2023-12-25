from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "9a19eae78f5d4c774b8e03cd0168117f7a20f4ad3eae0d0d4fbfbc12500374f6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
