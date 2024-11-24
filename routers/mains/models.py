from pydantic import BaseModel




class Automation(BaseModel):
    __table_name__ = "pay_automation"
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
    __table_name__ = "pay_automation_type"
    """
    types_automate_id - способ автоматизации, Ручной (1), Автоматический (2)
    """
    id: int
    title: str


class AutomationHistory(BaseModel):
    __table_name__ = "pay_automation_history"
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
    __table_name__ = "pay_automation_status"
    """
    status automate_status_id Активные (1), Успешные (2), Ошибка (2), Ошибка шаблона (3)
    """
    id: int
    title: str


class Bank(BaseModel):
    __table_name__ = "banks"
    """
    from yii2
    """
    id: int
    bik: str
    title: str


class Chart(BaseModel):
    __table_name__ = "chart"
    """
    from yii2
    """
    id: int
    title: str


class StatusReqs(BaseModel):
    __table_name__ = "pay_reqs_status"
    """
    status_reqs_id: Реквизит Активен (1) / не активен (0)
    """
    id: int
    title: str


class ReqsTypes(BaseModel):
    __table_name__ = "pay_reqs_types"
    """
    reqs.types - СБП / перевод с карты на карту / перевод по номеру счета...
    """
    id: int
    title: str


class Reqs(BaseModel):
    __table_name__ = "pay_reqs"
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


class ReqGroups(BaseModel):
    __table_name__ = "pay_reqs_groups"
    """
    types_automate_id: способ автоматизации Автоматический / ручной
    turn_off: автоматическое выключение реквизитов без доступа к автоматике
    """
    id: int
    reqs_id: int
    pay_id: int
    date: str
    title: str
    api_key_id: int
    types_automate_id: int
    turn_off: int


class Telegram(BaseModel):
    __table_name__ = "pay_telegram"
    """
    модуль для телеграма
    """
    id: int
    chat_id: str
    admin_id: str
    date: str


class RefsTypes(BaseModel):
    __table_name__ = "pay_refs_types"
    """
    Трейдеры, Магазины
    """
    id: int
    title: str


class Refs(BaseModel):
    __table_name__ = "pay_refs"
    """
    pay_referals from user
    level 0 по умолчанию 1 линия
    """
    id: int
    user_id: int
    referal_id: int
    level: int


class RefsLevel(BaseModel):
    __table_name__ = "pay_refs_level"
    """
    уровни рефералов %
    """
    id: int
    title: str
    value: float
