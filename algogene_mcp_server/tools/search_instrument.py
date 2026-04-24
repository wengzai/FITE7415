# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def search_instrument(
    symbols: str = "",
    desc: str = ""
) -> Dict[str, Any]:
    try:
        logger.info(f"Searching financial instruments")

        params = {}
        if symbols!="":
            params['symbols'] = str(symbols)
        if desc!="":
            params['desc'] = str(desc)

        status, res = utils._request("GET", url="/v1/search_instrument", data=params)
        logger.info(f"Successfully fetched related financial instruments")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in search_instrument tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

