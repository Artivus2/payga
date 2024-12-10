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
    from banks
    """
    id: int
    bik: str | None = None
    title: str | None = None
    address: str | None = None
    active: int | None = None


class BankFavs(BaseModel):
    __table_name__ = "pay_fav_banks"
    """
    from banks
    """
    id: int
    user_id: int
    bank_id: int | list



class Chart(BaseModel):
    __table_name__ = "chart"
    """
    from yii2
    """
    id: int
    title: str

class Currency(BaseModel):
    __table_name__ = "currency"
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
    id: int | None = None
    title: str


class ReqsTypes(BaseModel):
    __table_name__ = "pay_reqs_types"
    """
    reqs.types - СБП / перевод с карты на карту / перевод по номеру счета...
    """
    id: int = 0
    title: str | None = None


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
    limit_active_orders - количество одновременных ордеров минуты
    types_automate_id - способ автоматизации
    sequence - частота успешных ордеров
    status_reqs_id - Активен (1) / не активен (0)
    title - название
    """
    id: int | None = None
    uuid: str | None = None
    title: str | None = None
    user_id: int | None = None
    req_group_id: int = 0
    sequence: int = 1
    pay_pay_id: int | None = None
    value: str = '-'
    currency_id: int = 1
    reqs_types_id: int = 1
    reqs_status_id: int = 1
    bank_id: int | None = None
    phone: str = '+700000000'
    qty_limit_hour: int = 1
    qty_limit_day: int = 10
    qty_limit_month: int = 100
    sum_limit_hour: float = 1000
    sum_limit_day: float = 10000
    sum_limit_month: float = 100000
    limit_active_orders: int = 1
    other_banks:  int = 0
    min_sum_per_transaction: float = 0
    max_sum_per_transaction: float = 0
    max_limit_transaction_sum: float = 0
    max_limit_transaction: int = 0


class ReqsFilters(BaseModel):
    __table_name__ = "pay_reqs"
    """
    filters
    """
    id: int | None = None
    uuid: str | None = None
    title: str | None = None
    user_id: int | None = None
    req_group_id: int | None = None
    sequence: int | None = None
    pay_pay_id: int | None = None
    value: str | None = None
    currency_id: int | None = None
    reqs_types_id: int | None = None
    reqs_status_id: int | None = None
    bank_id: int | None = None
    phone: str | None = None
    qty_limit_hour: int | None = None
    qty_limit_day: int | None = None
    qty_limit_month: int | None = None
    sum_limit_hour: float | None = None
    sum_limit_day: float | None = None
    sum_limit_month: float | None = None
    limit_active_orders: int | None = None
    other_banks:  int | None = None
    min_sum_per_transaction: float | None = None
    max_sum_per_transaction: float | None = None
    max_limit_transaction_sum: float | None = None
    max_limit_transaction: int | None = None



class ReqToGroups(BaseModel):
    id_reqs: int | list | None = None
    id_group: int | None = None


class ReqGroups(BaseModel):
    __table_name__ = "pay_reqs_groups"
    """
    types_automate_id: способ автоматизации Автоматический / ручной
    turn_off: автоматическое выключение реквизитов без доступа к автоматике
    """
    id: int | None = None
    uuid: str | None = None
    reqs_id: int | None = None
    date: str | None = None
    title: str | None = None
    types_automate_id: int | None = None
    turn_off: int | None = None
    user_id: int | None = None


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
    id: int = 0
    title: str


class Refs(BaseModel):
    __table_name__ = "pay_refs"
    """
    pay_referals from user
    level 0 по умолчанию 1 линия
    """
    id: int | None = None
    user_id: int | None = None
    referal_id: int | None = None
    level: int | None = None


class RefsLevel(BaseModel):
    __table_name__ = "pay_refs_level"
    """
    уровни рефералов %
    """
    id: int | None = None
    title: str | None = None
    value: float | None = None
