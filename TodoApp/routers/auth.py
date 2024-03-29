import string
import sys

sys.path.append("..")
import random
from fastapi import Depends, HTTPException, status, APIRouter
from pydantic import BaseModel
from typing import Optional
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from TodoApp.res_forgot_password.res_forgot_pass import send_otp_email, send_fastapi_otp_email

SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str
    otp: str


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"user": "Not authorized"}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users) \
        .filter(models.Users.username == username) \
        .first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int,
                        expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=120)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username": username, "id": user_id}
    except JWTError:
        raise get_user_exception()


class SignUpRequest(BaseModel):
    email: str
    username: str


class ForgotPass(BaseModel):
    email: str


# Model for OTP verification request
class OTPVerificationRequest(BaseModel):
    email: str
    otp: str


class CreateNewPassword(BaseModel):
    email: str
    otp: str
    pass_word: str


otp_codes = {}


@router.post("/create/user")
async def sign_up(request: SignUpRequest, db: Session = Depends(get_db)):
    otp_code = ''.join(random.choices(string.digits, k=6))
    list_user_email_final = []
    list_user_email_username = []
    list_user_email = db.query(models.Users.email).all()
    list_user_username = db.query(models.Users.username).all()
    for data in list_user_email:
        list_user_email_final.append(data[0])
    for data in list_user_username:
        list_user_email_username.append(data[0])
    # print(list_user_email_final)
    # print(list_user_email_username)
    if request.email in list_user_email_final or request.username in list_user_username:
        raise http_exception()
    else:
        otp_codes[request.email] = otp_code
        if send_otp_email(request.email, otp_code):
            return {"message": "OTP code sent to email address."}
        raise get_user_exception()


@router.post("/forgot_pass")
async def forgot_pass(request: ForgotPass, db: Session = Depends(get_db)):
    otp_code = ''.join(random.choices(string.digits, k=6))
    list_user_email_final = []
    list_user_email = db.query(models.Users.email).all()
    for data in list_user_email:
        list_user_email_final.append(data[0])
    if request.email not in list_user_email_final:
        raise http_exception()
    else:
        otp_codes[request.email] = otp_code
        if send_otp_email(request.email, otp_code):
            return {"message": "OTP code sent to email address."}
        raise get_user_exception()


@router.post("/verify")
def verify(create_user: CreateUser, db: Session = Depends(get_db)):
    create_user_model = models.Users()
    if check_data_username(create_user.username) and check_data_other(create_user.email) and check_data_other(
            create_user.username) and check_data_other(create_user.last_name):
        create_user_model.email = create_user.email
        if create_user_model.email not in otp_codes:
            raise HTTPException(status_code=400, detail="OTP code not found.")
        if otp_codes[create_user.email] != create_user.otp:
            raise HTTPException(status_code=400, detail="Invalid OTP code.")
        create_user_model.username = create_user.username
        create_user_model.first_name = create_user.first_name
        create_user_model.last_name = create_user.last_name
        hash_password = get_password_hash(create_user.password)
        create_user_model.hashed_password = hash_password
        create_user_model.is_active = True
        db.add(create_user_model)
        db.commit()
        db.close()
    else:
        raise token_exception()

    return {"message": "OTP code verified."}


@router.put("/create_new_pass")
async def create_new_pass(create_new_pass: CreateNewPassword, db: Session = Depends(get_db)):
    # create_user_model = models.Users()
    create_pass_model = db.query(models.Users) \
        .filter(models.Users.email == create_new_pass.email) \
        .first()
    print(create_pass_model)
    if check_data_username(create_new_pass.pass_word):
        print('1')
        create_pass_model.email = create_new_pass.email
        if create_pass_model.email not in otp_codes:
            raise HTTPException(status_code=400, detail="OTP code not found.")
        if otp_codes[create_new_pass.email] != create_new_pass.otp:
            raise HTTPException(status_code=400, detail="Invalid OTP code.")
        create_pass_model.hashed_password = get_password_hash(create_new_pass.pass_word)
        db.add(create_pass_model)
        db.commit()
        db.close()
    else:
        raise token_exception()
    return {"message": "Change password."}


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=360)
    token = create_access_token(user.username,
                                user.id,
                                expires_delta=token_expires)
    return {"token": token}


# Exceptions
def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception


def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_exception_response


def check_data_username(data):
    if data != '' and ' ' not in str(data):
        return True
    return False


def check_data_other(data):
    if data != '':
        return True
    return False


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")
