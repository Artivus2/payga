from pydantic import BaseModel


class Status(BaseModel):
    """
    status: Активны, успешные, отмененные
    """
    id: int
    title: str


class Orders(BaseModel):
    """
    req_type = reqs.id
    status: Активны, успешные, отмененные
    pay: Payin (0), Payout (1)
    """
    id: int
    uuid: str
    course: float
    sum_fiat: float
    pay_id: int
    percent: float
    cashback: float
    date: int
    date_expiry: int
    req_id: int
    status_id: int
    docs_id: int


class Cashback(BaseModel):
    """
    title Название кешбека
    group_user_id: группа пользователей (Трейдеры, Магазины..)
    status: действует
    """
    id: int
    title: str
    date: int
    group_user_id: int
    percent: float
    status: int

class Docs(BaseModel):
    """
    Квитанции (image)
    """
    id: int
    order_id: int
    url: str

