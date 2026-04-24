# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def strategy_market_perf(
    symbol: str,
    startDate: str,
    endDate: str
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching performance statistics for market index: {symbol}")

        params = {
            "symbol": str(symbol),
            "startDate": str(startDate),
            "endDate": str(endDate)
        }

        status, res = utils._request("GET", url="/v1/strategy_market_perf", data=params)
        logger.info(f"Successfully fetched performance statistics for market index: {symbol}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in strategy_market_perf tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

