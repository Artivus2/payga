from pydantic import BaseModel


class Orders(BaseModel):
    __table_name__ = "pay_orders"
    """
    status: pay_notify_order_types
    pay: Payin (0), Payout (1)
    """
    id: int | None = None
    order_id: int | None = None
    user_id: int | None = None
    course: float | None = None
    chart_id: int | None = None
    pay_id: int | None = None
    value: float | None = None
    sum_fiat: float | None = None
    cashback: float | None = None
    date: str | None = None
    date_expiry: str | None = None
    req_id: int | None = None
    pay_notify_order_types_id: int | list | None = None
    docs_id: int | list | None = None
    date_start: str | None = None
    date_end: str | None = None



class CashbackStatus(BaseModel):
    __table_name__ = "pay_cashback_status"
    """
    status: действует (1), не действует (0)
    """

    id: int
    title: str | None = None


class Cashback(BaseModel):
    __table_name__ = "pay_cashback"
    """
    title Название кешбека
    group_user_id: группа пользователей (Трейдеры, Магазины..)
    status: действует
    """
    id: int | None
    title: str | None
    date: str | None
    pay_reqs_group_id: int | None
    value: float | None
    status_id: int | None


class Docs(BaseModel):
    __table_name__ = "pay_docs"
    """
    Квитанции (image)
    """
    #id: int
    order_id: int
    url: str

