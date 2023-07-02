import requests
from datetime import datetime, timedelta

from app.config import settings
from app.schemas import TatumApiEthTransaction


def tatum_api_headers():
    return {"x-api-key": f"{settings.tatum_api_key}"}


def get_txs_for_address(address: str, offset: int = 0, limit: int = 50):
    url = f"{settings.tatum_api_url}/ethereum/account/transaction/{address}"
    query = {
        "pageSize": min(50, limit),
        "offset": offset
    }
    response = requests.get(url, headers=tatum_api_headers(), params=query)
    txs_with_timestamp: list[TatumApiEthTransaction] = [TatumApiEthTransaction.parse_obj(tx) for tx in response.json()]
    period_start = (datetime.utcnow() - timedelta(days=settings.txs_period_days)).timestamp()
    non_outdated_txs = [
        {
            "transactionHash": tx.transactionHash,
            "blockHash": tx.blockHash,
        }
        for tx in txs_with_timestamp if tx.timestamp >= period_start
    ]
    return non_outdated_txs
