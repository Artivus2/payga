from pydantic import BaseModel


class Role(BaseModel):
    """
    Группы пользователей (Трейдеры, Магазины, Оператор, администратор)
    """
    id: int
    roles: str
    pages: list