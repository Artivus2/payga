from pydantic import BaseModel


class Orders(BaseModel):
    __table_name__ = "pay_orders"
    """
    status: pay_notify_order_types
    pay: Payin (0), Payout (1)
    """
    id: int | None = None
    user_id: int | None = None
    course: float | None = None
    chart_id: int | None = None
    sum_fiat: float | None = None
    pay_id: int | None = None
    value: float | None = None
    cashback: float | None = None
    date: str | None = None
    date_expiry: str | None = None
    req_id: int | None = None
    pay_notify_order_types_id: int | list | None = None
    docs_id: int | list | None = None



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
    #id: int
    order_id: int
    url: str

