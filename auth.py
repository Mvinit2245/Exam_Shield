from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "secretkey"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# ✅ CREATE TOKEN
def create_token(data: dict):
    to_encode = data.copy()
    to_encode.update({
        "exp": datetime.utcnow() + timedelta(hours=2)
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ✅ VERIFY TOKEN (FIXED)
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except Exception as e:
        print("TOKEN ERROR:", str(e))   # 🔥 DEBUG
        raise HTTPException(status_code=401, detail="Invalid token")