#5. Fetch  user details
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import models, schemas, security
from app.db import get_db
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

def get_user(db: Session, username:str):
    # this line performs database query on User table of db and retrieves first username from User table
    return db.query(models.User).filter(models.User.username== username).first()




async def get_current_user(
    token: str = Depends(oauth2_scheme), db:Session= Depends(get_db)
):
    credential_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could no t validate credentials",
        headers = {"WWW-Authentiicate":"Bearer"},
    )
    try: 
        # here it decodes the token based on security key and algorithm
        payload = jwt.decode(
            # security is a python script. We are pulling secrey key and algorithm from that file
            token, security.SECRET_KEY, algorithms= [security.ALGORITHM]
        )
        username:str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = schemas.TokenData(username = username)
    except JWTError:
        raise credential_exception
    user = get_user(db, username = token_data.username)
    if user is None:
        raise credential_exception
    return user




'''
How does the get_current_user work?
when this function is invoked it gets token and database datas.
After receiving it decodes the token based on security key and algorithm defined in security.py and
fetches username. and if thee is no username then it throws exception.
'''