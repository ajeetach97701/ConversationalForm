from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


import os


from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from app import auth, models, schemas, security
from ai.prompts import generate_context, qa_template
from app.models import User
from app.db import get_db
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



router = APIRouter()


@router.post("/register/", response_model = schemas.UserInDBBase)
async def register(user_in: schemas.UserIn, db:Session=  Depends(get_db)):
    db_user = auth.get_user(db, username = user_in.username)
    if db_user:
        raise HTTPException(status_code = 400, detail = "Username already registered")
    db_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if db_user:
        raise HTTPException(status_code = 400, detail = "Email already registerd")
    
    hashed_password = security.get_password_hash(user_in.password)
    db_user = models.User(**user_in.dict(exclude={"password"}), hashed_password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/token", response_model = schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)
):
    user = auth.get_user(db,username = form_data.username)
    if not user or not security.pwd_context.verify(
        form_data.password,user.hashed_password
    ):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password",
            headers = {"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes = security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data = {"sub":user.username}, expires_delta = access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/conversation/")
async def read_conversation(
    query:str,
    current_user : schemas.UserInDB = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    db_user = db.query(User).get(current_user.id)
    if not db_user:
        raise HTTPException(status_code = 404, details = "User not found")
    context = generate_context(db_user)
    llm = OpenAI(
        temperature = 0,
        openai_api_key = OPENAI_API_KEY,
    )
    prompt = PromptTemplate(
        input_variables = ["context","question "], template = qa_template
    )
    chain = LLMChain(llm = llm, prompt = prompt)
    response = chain.run(context  = context, question = query)
    return {"response":response}