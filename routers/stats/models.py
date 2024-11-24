from pydantic import BaseModel

class Statistic(BaseModel):
    __table_name__ = "pay_stats"
    """
    статистика
    """
    id: int
    title: str