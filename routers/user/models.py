from pydantic import BaseModel


class Role(BaseModel):
    pass


class User(BaseModel):
    login: str
    email: str
    password: str
    telegram: str
    affiliate_invitation_id: int


class Logout(BaseModel):
    token: str


class RegisterRequest(BaseModel):
    id: int
    login: str


class Login(BaseModel):
    email: str
    password: str


class Code(BaseModel):
    email: str
    password: str
    code: str


class JwtRequest(BaseModel):
    email: str
    password: str


class Twofa(BaseModel):
    code: str