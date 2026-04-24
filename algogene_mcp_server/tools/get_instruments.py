# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_instruments() -> Dict[str, Any]:
    try:
        logger.info(f"Fetching available trading instruments")

        params = {}
        status, res = utils._request("GET", url="/v1/list_instrument", data=params)
        logger.info(f"Successfully fetched available trading instruments")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_instruments tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

