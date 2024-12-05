from pydantic import BaseModel

class Statistic(BaseModel):
    __table_name__ = "pay_stats"
    """
    статистика
    """
    user_id: int | None = None
    title: str | None = None