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
    id: int | None = None
    title: str | None = None


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


class ReqsStatus(BaseModel):
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


class AutomationTurnOff(BaseModel):
    __table_name__ = "pay_automation_turn_off"
    """
    автоматическое выключение реквизитов без доступа к автоматике (1 - включено, 0 - выключено)
    """
    id: int
    title: str


class Reqs(BaseModel):
    __table_name__ = "pay_reqs"
    """
    value - номер карты / счета
    reqs_types - Способ оплаты (СБП / перевод с карты на карту / перевод по номеру счета...)
    bank_id - банк
    currency_id - валюта
    phone - телефон
    pay_id: Payin - 0, Payout - 1
    req_group_id - ид группы реквизитов
    qty - лимит сделок в час / день / месяц
    sum - лимит сумм в час / день / месяц
    types_automate_id - способ автоматизации
    sequence - частота успешных ордеров
    status_reqs_id - Активен (1) / не активен (0)
    """
    uuid: str | None = None
    user_id: int
    req_group_id: int | None = None
    sequence: int | None = None
    pay_pay_id: int | None = None
    value: str | None = None
    currency_id: int | None = None
    reqs_types_id: int | None = None
    reqs_status_id: int | None = None
    bank_id: int | None = None
    chart_id: int | None = None
    phone: str | None = None
    date: int | None = None
    qty_limit_hour: int | None = None
    qty_limit_day: int | None = None
    qty_limit_month: int | None = None
    sum_limit_hour: float | None = None
    sum_limit_day: float | None = None
    sum_limit_month: float | None = None



class ReqGroups(BaseModel):
    __table_name__ = "pay_reqs_groups"
    """
    types_automate_id: способ автоматизации Автоматический / ручной
    turn_off: автоматическое выключение реквизитов без доступа к автоматике
    """
    id: int
    uuid: str | None = None
    reqs_id: int | None = None
    date: str | None = None
    title: str | None = None
    automation_type_id: int | None = None
    turn_off: int | None = None


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
