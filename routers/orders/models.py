from pydantic import BaseModel


class Orders(BaseModel):
    __table_name__ = "pay_orders"
    """
    req_type = reqs.id
    status: pay_notify_order_types
    pay: Payin (0), Payout (1)
    """
    id: int
    uuid: str
    course: float
    sum_fiat: float
    pay_id: int
    percent: float
    cashback: float
    date: str
    date_expiry: str
    req_id: int
    pay_notify_order_types_id: int
    docs_id: int


class CashbackStatus(BaseModel):
    __table_name__ = "pay_cashback_status"
    """
    status: действует, не действует
    """

    id: int
    title: str


class Cashback(BaseModel):
    __table_name__ = "pay_cashback"
    """
    title Название кешбека
    group_user_id: группа пользователей (Трейдеры, Магазины..)
    status: действует
    """
    id: int
    title: str
    date: str
    group_user_id: int
    value: float
    status_id: int


class Docs(BaseModel):
    __table_name__ = "pay_docs"
    """
    Квитанции (image)
    """
    id: int
    order_id: int
    url: str

