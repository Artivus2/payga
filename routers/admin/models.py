from fastapi import HTTPException
from pydantic import BaseModel
from starlette.requests import Request

class ConfirmRegister(BaseModel):
    """
    user
    """
    user_id: int | None = None
    login: str | None = None
    email: str | None = None


class Status(BaseModel):
    __table_name__ = "pay_admin_role_status"
    """
    +
    status: Активна (1), не активна (2)
    """
    id: int
    title: str


class Methods(BaseModel):
    __table_name__ = "pay_admin_methods"
    """
    +
    Все методы
    """
    id: int
    title: str
    status: int


class Pages(BaseModel):
    __table_name__ = "pay_admin_pages"
    """
    +
    страницы
    """
    id: int
    title: str
    status: int


class Role(BaseModel):
    __table_name__ = "pay_admin_roles"
    """
    Группы пользователе
    + (Трейдер, Магазин, Оператор, администратор)
    """
    id: int | None = None
    title: str | None = None
    pages: int | None = None
    status: int | None = None


class Allowed(BaseModel):
    __table_name__ = "pay_admin_roles_allowed"
    """
    +
    Доступна (1), Не доступна (0)
    """
    id: int
    title: str

class AuthRoles(BaseModel):
    __table_name__ = "user"
    """
    +
    привязка к группе методов ролей user страниц
    """
    id: int | None = None
    user_id: int | None = None
    role_id: int | None = None
    # method_id: int | None = None
    # page_id: int | None = None
    # status: int | None = None
    # pay_admin_roles_allowed: int | None = None


class Sms(BaseModel):
    """
    sms receiver
    """
    from1: str | None = None
    text: str | None = None
    sentStamp: str | None = None
    receivedStamp: str | None = None
    sim: str | None = None
    api_key: str | None = None


class Invoice(BaseModel):
    __table_name__ = "pay_invoice"
    id: int | None = None
    req_id: int | None = None
    sum_fiat: float | None = None
    api_key: str | None = None


class Parsers(BaseModel):
    id: int | None = None
    shablons: str | None = None
    sender: str | None = None


class ApiStatus(BaseModel):
    id: int | None = None

