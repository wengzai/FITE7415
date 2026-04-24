# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_history_price(
    instrument: str,
    interval: str,
    count: int,
    timestamp: str,
    chain_dated: int = 0,
    expiry: str = "",
    right: str = "", 
    strike: float = 0
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching historical market price for instrument: {instrument}")

        params = {
            "instrument": str(instrument),
            "interval": str(interval),
            "count": int(count),
            "timestamp": str(timestamp)
        }
        if expiry!="":
            params['expiry'] = str(expiry)
        if right!="":
            params['right'] = str(right)
        if strike!=0:
            params['strike'] = float(strike)
        if chain_dated>0:
            params['chain_dated'] = int(chain_dated)
        status, res = utils._request("GET", url="/v1/history_price", data=params)

        logger.info(f"Successfully fetched historical market price for {instrument}: {res}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_history_price tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

