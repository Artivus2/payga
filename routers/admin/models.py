from pydantic import BaseModel


class ConfirmRegister(BaseModel):
    """
    user
    """
    user_id: int
    login: str
    email: str


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
    + (Трейдеры, Магазины, Оператор, администратор)
    """
    id: int
    title: str
    pages: int
    status: int


class Allowed(BaseModel):
    __table_name__ = "pay_admin_roles_allowed"
    """
    +
    Доступна (1), Не доступна (0)
    """
    id: int
    title: str

class AuthRoles(BaseModel):
    __table_name__ = "pay_admin_auth_roles"
    """
    +
    привязка к группе методов ролей user страниц
    """
    id: int | None
    user_id: int | None
    role_id: int | None
    method_id: int | None
    page_id: int | None
    status: int | None
    pay_admin_roles_allowed: bool | None






