from pydantic import BaseModel

class Notification(BaseModel):
    __table_name__ = "pay_notification"
    """
    notification
    """
    id: int | None = None
    user_id: int | None = None
    message: str | None = None
    date: str | None = None
    status: str | None = None