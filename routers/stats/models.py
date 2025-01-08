from pydantic import BaseModel

class Statistic(BaseModel):
    __table_name__ = "pay_stats"
    """
    статистика
    """
    user_id: int | None = None
    title: str | None = None
    date_begin:str | None = None
    date_end: str | None = None
    pay_id:  int | None = None