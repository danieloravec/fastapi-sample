from pydantic import BaseModel


class TatumApiEthTransaction(BaseModel):
    blockHash: str
    timestamp: int
    transactionHash: str
