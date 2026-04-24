# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_history_corp_announcement(
    symbol: str,
    starttime: str,
    endtime: str,
    event: str = ""
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching corporate announcement history for symbol: {symbol}")

        params = {
            "symbol": str(symbol),
            "starttime": str(starttime),
            "endtime": str(endtime),
            "event": str(event)
        }
        status, res = utils._request("GET", url="/v1/history_corp_announcement", data=params)
        logger.info(f"Successfully fetched corporate announcement history for symbol: {symbol}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_history_corp_announcement tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

