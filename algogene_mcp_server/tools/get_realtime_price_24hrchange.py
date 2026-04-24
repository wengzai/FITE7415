# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_realtime_price_24hrchange(
    symbols: List[str]
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching 24hr price change for symbol: {symbols}")

        params = {
            "symbols": ",".join(symbols)
        }
        status, res = utils._request("GET", url="/v1/realtime_price_24hrchange", data=params)

        logger.info(f"Successfully fetched 24hr price change for {symbols}: {res}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_realtime_price_24hrchange tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

