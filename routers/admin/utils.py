import json
import secrets
import string
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import config
import pyotp




## To verify the OTP given by the user generated by the Authenticator
@staticmethod
def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)

## ---------------------------- Hashing --------------------------------
## For password encryption and verfications
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# async def create_random_key(length: int = 8) -> str:
#     return "12345678"

async def create_random_key(length: int = 8) -> str:
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return "".join(secrets.choice(chars) for _ in range(length))


async def verify(plain, hashed):
    return pwd_context.verify(plain, hashed)


async def get_hash(value):
    return pwd_context.hash(value)


## Checking if the JWT token is used before and the user is no longer active
def find_token_black_lists(token: str):
    token = None
    # check blists
    return True if token else False

##---------------------------- oauth2 --------------------------------
## Login for token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_token_user(token: str = Depends(oauth2_scheme)):
    return token


## Creating access token by embedding the user details and the expiration timestamp
def create_access_token(*, user_id: str, role: int, expires_delta: int):
    to_encode = {"user_id": user_id,
                 "role": role,
                 "expiration": (datetime.now() + timedelta(minutes=expires_delta)).strftime("%Y-%m-%d %H:%M:%S")}

    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)

    return encoded_jwt



# async def send_email_yii2(login, email):
#     """
#     отправить почту пользователю
#     :param login, email:
#     :return:
#     """
#     api_url = f'{config.BASE_URL}/api/user/send-email'
#     headers = {
#         'Content-Type': 'application/json',
#     }
#     payload = {
#         'login': login,
#         'email': email
#     }
#     response = requests.post(api_url, headers=headers, data=json.dumps(payload))
#     if response.status_code != 200:
#         raise HTTPException(status_code=response.status_code, detail=response.json())
#     return response.json()

async def send_email(email):
    pass



