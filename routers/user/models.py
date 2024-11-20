from pydantic import BaseModel

class User(BaseModel):
    """
    все понятно
    """
    id: int
    login: str
    email: str
    password: str
    telegram: str
    affiliate_invitation_id: int


class ApiKeyStatus(BaseModel):
    """
    status: Активный, Неактивныый, Удален, просрочен
    """

class ApiKey(BaseModel):
    """
    Status: Валидный (1), Не валидный (0)
    api_key - ключ для АПИ пользователя
    __pay_api_keys__
    """
    id: int | None = None
    user_id: int
    api_key: str | None = None
    api_key_begin_date: str | None = None
    api_key_expired_date: str | None = None
    status: int | None = None

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
    email: str | None
    password: str | None
    token: str | None
    user_id: int


class Twofa(BaseModel):
    token: str
    user_id: int | None = None
    secret: str | None = None



