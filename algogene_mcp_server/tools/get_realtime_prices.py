# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_realtime_prices(
    symbols: List[str],
    broker: str = ""
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching market price for symbol: {symbols}")

        # Original version:
        # params = {
        #     "symbols": ",".join(symbols),
        #     "broker": str(broker)
        # }
        params = {}
        if len(symbols) == 1:
            params["symbol"] = symbols[0]
        else:
            params["instruments"] = ",".join(symbols)
        if broker:
            params["broker"] = str(broker)
        status, res = utils._request("GET", url="/v1/realtime_price", data=params)

        logger.info(f"Successfully fetched market price for {symbols}: {res}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_realtime_prices tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

