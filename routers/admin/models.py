from pydantic import BaseModel


class ConfirmRegister(BaseModel):
    user_id: int
    login: str
    email: str
