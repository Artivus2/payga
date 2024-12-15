from pydantic import BaseModel


class Withdraws(BaseModel):
    """
    хз пока
    """
    id: int | None = None
    title: str | None = None


class WalletAddress(BaseModel):
    id: int | None = None
    user_id: int | None = None
    chain_id: int | None = None
    value: str | None = None
    private_key: str | None = None
    public_key: str | None = None
    hex_address: str | None = None
