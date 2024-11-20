from pydantic import BaseModel




class Automation(BaseModel):
    """
    status = automation_status_id
    """
    id: int
    uuid: str
    order_id: int
    text: str
    title: str
    types_automate_id: int
    automation_status_id: int


class TypesAutomate(BaseModel):
    """
    types_automate_id - способ автоматизации, Ручной (0), Автоматический (1)
    """
    id: int
    title: str


class AutomationHistory(BaseModel):
    """
    status = automation_status_id
    text: текст сообщения
    types: способ автоматизации
    automate_status_id: Активные, Успешные, Ошибка, Ошибка шаблона

    """
    id: int
    automation_id: int
    order_id: int
    text: str
    types_automate_id: int
    automate_status_id: int


class AutomationStatus(BaseModel):
    """
    status automate_status_id Активные, Успешные, Ошибка, Ошибка шаблона
    """
    id: int
    title: str


class Bank(BaseModel):
    """
    from yii2
    """
    id: int
    bik: str
    title: str


class Chart(BaseModel):
    """
    from yii2
    """
    id: int
    title: str


class StatusReqs(BaseModel):
    """
    status_reqs_id: Реквизит Активен (1) / не активен (0)
    """
    id: int
    title: str


class ReqsTypes(BaseModel):
    """
    reqs.types - СБП / перевод с карты на карту / перевод по номеру счета...
    """
    id: int
    title: str


class Reqs(BaseModel):
    """
    value - номер карты / счета
    reqs_types - Способ оплаты (СБП / перевод с карты на карту / перевод по номеру счета...)
    bank_id - банк
    chart - валюта
    phone - телефон
    pay_id: Payin - 0, Payout - 1
    req_group_id - ид группы реквизитов
    qty - лимит сделок в час / день / месяц
    sum - лимит сумм в час / день / месяц
    types_automate_id - способ автоматизации
    sequence - частота успешных ордеров
    status_reqs_id - Активен (1) / не активен (0)
    """
    uuid: str
    user_id: int
    req_group_id: int
    sequence: int
    pay_id: int
    value: str
    reqs_types_id: int
    bank_id: int
    chart_id: int
    phone: str
    date: int
    qty_limit_hour: int
    qty_limit_day: int
    qty_limit_month: int
    sum_limit_hour: float
    sum_limit_day: float
    sum_limit_month: float
    status_reqs_id: int


class ReqGroup(BaseModel):
    """
    types_automate_id: способ автоматизации Автоматический / ручной
    turn_off: автоматическое выключение реквизитов без доступа к автоматике
    """
    id: int
    reqs_id: int
    pay_id: int
    date: int
    title: str
    api_key_id: int
    types_automate_id: int
    turn_off: int


class Telegram(BaseModel):
    """
    модуль для телеграма
    """
    id: int
    chat_id: str
    admin_id: str
    date: int


class RefsTypes(BaseModel):
    """
    Трейдеры, Магазины
    """
    id: int
    title: str

class Refs(BaseModel):
    """
    pay_referals from user
    level 0 по умолчанию 1 линия
    """
    id: int
    user_id: int
    ref_token: str
    referal_id: int
    level: int

