# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def list_econs_series() -> Dict[str, Any]:
    try:
        logger.info(f"Fetching available economic time series ID")

        params = {}
        status, res = utils._request("GET", url="/v1/list_econs_series", data=params)
        logger.info(f"Successfully fetched available economic time series")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in list_econs_series tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

