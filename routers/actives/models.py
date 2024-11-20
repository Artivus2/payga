from pydantic import BaseModel


class Pay(BaseModel):
    """
    Payin, Payout
    """
    id: int
    title: str


class PayStatus(BaseModel):
    """
    Действующий (1), не действующий (0)
    """
    id: int
    title: str


class PayPercent(BaseModel):
    """
    pay_id in Pay
    """
    id: int
    user_id: int
    pay_id: int
    percent: float
    date: int
    pay_status_id: int


class BalanceStatus(BaseModel):
    """
    title: 0 - доступно, 1 - заморожено
    """
    id: int
    title: str

class BalanceTypes(BaseModel):
    """
    title: 0 - активные, 1 - архивные
    """
    id: int
    title: str


class Balance(BaseModel):
    """
    balance_types: 0 - активные, 1 - архивные
    balance_status: 0 - доступно, 1 - заморожено
    """
    id: int
    user_id: int
    value: float
    mains_chart_id: int
    balance_status_id: int
    balance_types_id: int


class BalanceHistory(BaseModel):
    """
    description - Основание
    """
    id: int
    user_id: int
    balance_id: int
    chart: str
    date: int
    value: float
    balance_status_id: int
    balance_types_id: int
    description: str


class Deposit(BaseModel):
    """
    types: 0 - активные, 1 - архивные
    status: 0 - доступно, 1 - заморожено
    """
    id: int
    value: float
    user_id: int
    status: int
    types: int


class WalletStatus(BaseModel):
    """
    Активный / не активный
    """
    id: int
    title: str

class Wallet(BaseModel):
    """
    крипто кошелек
    """
    id: int
    user_id: int
    network: str
    address: str
    wallet_status: int
    date: int


class TransferStatus(BaseModel):
    """
    status: исполнен, отменен
    """
    id: int
    title: str


class Transfer(BaseModel):
    """
    status: 0 - активные, 1 - архивные
    """
    id: int
    user_id_in: int
    user_id_out: int
    value: float
    status: int


class Exchange(BaseModel):
    id: int
    chart_in_id: int
    chart_out_id: int
    date: int
    value: float
    course: float # from todo

