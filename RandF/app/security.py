# 4. CREATE AN ACCESS TOKEN

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

from passlib.context import CryptContext

SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# object of CryptContext
pwd_context = CryptContext(schemes =["bcrypt"], deprecated = "auto")

#bcrypt is an algorithm for hashing password. It is resistact to brute-force attacks.
# deprecated = "auto" when set to auto it will automatically handle deprecated hashing 
# schemes

# This function actually hashes the password
def get_password_hash(password:str):
    return pwd_context.hash(password)


def create_access_token(* , data:dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta: 
        expire = datetime.utcnow() + expires_delta
    else:
         expire = datetime.utcnow() +  + timedelta(minutes=15)
    to_encode.update({"exp": expire}) 
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt
    # this line jwt.encode encodes the to_encode dictionary into a jwt using 
    # jwt.encode function .
    # SECRET_KEY is used as the secret key for signing the token using the ALGORITHM
    