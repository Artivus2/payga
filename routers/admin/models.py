from pydantic import BaseModel


class Role(BaseModel):
    roles: str


class ConfirmRegister(BaseModel):
    user_id: int
    login: str
    email: str
