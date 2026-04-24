# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_realtime_econs_stat() -> Dict[str, Any]:
    try:
        logger.info(f"Fetching most recently released economic statistics")

        params = {}
        status, res = utils._request("GET", url="/v1/realtime_econs_stat", data=params)
        logger.info(f"Successfully fetched most recently released economic statistics")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_realtime_econs_stat tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

