from pydantic import BaseModel


class Pay(BaseModel):
    __table_name__ = "pay_pay"
    """
    +
    Payin (1), Payout (2)
    """
    id: int
    title: str


class PayStatus(BaseModel):
    __table_name__ = "pay_pay_status"
    """
    +
    Действующий (1), не действующий (2) , 0 - все
    """
    id: int
    title: str


class PayPercent(BaseModel):
    __table_name__ = "pay_pay_percent"
    """
    +
    pay_id in Pay
    pay_status_id in status_id
    """
    id: int | None
    user_id: int | None
    pay_id: int | None
    value: float | None
    date: str | None
    pay_status_id: int | None


class BaldepStatus(BaseModel):
    __table_name__ = "pay_baldep_status"
    """
    +
    title: 1 - доступно, 2 - заморожено
    """
    id: int
    title: str

class BaldepTypes(BaseModel):
    __table_name__ = "pay_baldep_types"
    """
    +
    title: 0 - активные, 1 - архивные
    """
    id: int
    title: str


class Balance(BaseModel):
    __table_name__ = "pay_balance"
    """
    +
    balance_status: 1 - доступно, 0 - заморожено
    balance_types: 1 - активные, 0 - архивные
    """
    id: int | None
    user_id: int | None
    value: float | None
    chart_id: int | None
    baldep_status_id: int | None
    baldep_types_id: int | None
    date: str | None


class BalanceHistory(BaseModel):
    __table_name__ = "pay_balance_history"
    """
    +
        description - Основание
    """

    id: int
    user_id: int
    balance_id: int
    chart: str
    date: str
    value: float
    baldep_status_id: int
    baldep_types_id: int
    description: str


class Deposit(BaseModel):
    __table_name__ = "pay_deposit"
    """
    +
    types: 0 - активные, 1 - архивные
    status_id: 0 - доступно, 1 - заморожено
    """
    id: int
    user_id: int
    value: float
    baldep_status_id: int
    baldep_types_id: int
    description: str


class WalletStatus(BaseModel):
    __table_name__ = "pay_wallet_status"
    """
    +
    Активный (1) / не активный (2)
    """
    id: int
    title: str


class Wallet(BaseModel):
    __table_name__ = "pay_wallet"
    """
    +
    крипто кошелек
    """
    id: int
    user_id: int
    network: str
    address: str
    wallet_status: int
    date: str


class TransferStatus(BaseModel):
    __table_name__ = "pay_transfer_status"
    """
    +
    status: исполнен (1), отменен (2), в ожидании (3)
    """
    id: int = 0
    title: str | None = None


class TransferHistory(BaseModel):
    __table_name__ = "pay_transfer_history"
    """
    +
    status: 0 - активные, 1 - архивные
    """
    id: int
    user_id_in: int
    user_id_out: int
    value: float
    status: int
    date: str


class ExchangeHistory(BaseModel):
    __table_name__ = "pay_exchange_history"
    """
    +
    """
    id: int
    chart_in_id: int
    chart_out_id: int
    value: float
    course: float # from todo
    date: str

