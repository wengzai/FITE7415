# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_realtime_exchange_rate(
    cur1: str,
    cur2: str
) -> Dict[str, float]:
    try:
        logger.info(f"Fetching exchange rate: {cur1} to {cur2}")

        params = {
            "cur1": str(cur1),
            "cur2": str(cur2)
        }
        status, res = utils._request("GET", url="/v1/realtime_exchange_rate", data=params)

        logger.info(f"Successfully fetched exchange rate from {cur1} to {cur2}: {res}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_realtime_exchange_rate tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

