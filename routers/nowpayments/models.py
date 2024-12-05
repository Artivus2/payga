from pydantic import BaseModel


class CreatePaymentRequest(BaseModel):
    amount: float
    currency: str
    order_id: str
    pay_currency: str


class CreatePayoutRequest(BaseModel):
    amount: float
    currency: str
    address: str


class JwtRequest(BaseModel):
    email: str
    password: str