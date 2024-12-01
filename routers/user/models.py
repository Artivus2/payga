import datetime
from pydantic import BaseModel




class User(BaseModel):
    __table_name__ = "user"
    """
    Пользователь из yii2
    """
    id: int | None = None
    login: str | None = None
    email: str | None = None
    password: str | None = None
    telegram: str | None = None
    affiliate_invitation_code: str | None = None
    is_active: int | None = None
    role_id: int | None = None
    banned: int | None = None


class JwtTokenSchema(BaseModel):
    token: str
    payload: dict | None
    expire: datetime.datetime | None


class Blacklists(BaseModel):
    __tablename__ = 'blacklists'
    id: int
    token: str
    email: str


class TokenPair(BaseModel):
    access: JwtTokenSchema
    refresh: JwtTokenSchema


class Profile(BaseModel):
    __table_name__ = "user"
    #todo добавить telegram_connected, twofa_status
    """
    +
    Профиль
    """
    user_id: int
    email: str
    login: str
    telegram: str
    banned: int
    verify_status: int
    created_at: str
    telegram_connected: int
    twofa_status: int


class NotifyTypes(BaseModel):
    __table_name__ = "pay_notify_types"
    """
    +
    type 0 - payin, 1- payout 2 - автоматика
    """
    id: int
    title: str
    type: int


class NotifyUserSettings(BaseModel):
    __table_name__ = "pay_notify_user_settings"
    """
    +
    Настройки уведомлений по ордерам
    status (0) выключен, (1) - включен
    """
    id: int
    user_id: int
    notify_type_id: int
    status_id: int


class ApiKeyStatus(BaseModel):
    __table_name__ = "pay_api_keys_status"
    """
    +
    status: Активный, Не активный, Удален, просрочен
    """
    id: int
    title: str


class ApiKey(BaseModel):
    __table_name__ = "pay_api_keys"
    """
    +
    Status: Валидный (1), Не валидный (0)
    api_key - ключ для АПИ пользователя
    __pay_api_keys__
    """
    id: int | None = None
    user_id: int | None = None
    api_key: str | None = None
    api_key_begin_date: str | None = None
    api_key_expired_date: str | None = None
    status_id: int | None = None
    code:  int | None = None
    email:  str | None = None
    fcm_token: str | None = None
    access_token: str | None = None



class Logout(BaseModel):
    token: str


class RegisterRequest(BaseModel):
    id: int
    login: str


class Login(BaseModel):
    email: str
    login: str | None = None
    password: str


class Code(BaseModel):
    __table_name__ = "auth_tokens"
    """
    запрос в auth_tokens yii2
    """
    email: str
    password: str
    code: str


class JwtRequest(BaseModel):
    __table_name__ = "auth_tokens"
    """
    запрос в auth_tokens from yii2
    """
    email: str | None
    password: str | None
    token: str | None
    user_id: int


class Twofa(BaseModel):
    __table_name__ = "user_two_factor"
    """
    user.twofa
    """
    id: int
    user_id: int | None = None
    secret: str | None = None
    date: int
    status: int



## ---------------------------------  2FA ---------------------------------
class LoginOTP(BaseModel):
    email: str
    otp: int

class Enable2FA(BaseModel):
    otp: int