from pydantic import BaseModel


class Withdraws(BaseModel):
    """
    хз пока
    """
    id: int | None = None
    title: str | None = None
