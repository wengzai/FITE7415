# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_history_econs_calendar(
    starttime: str,
    endtime: str
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching upcoming economic calendar")

        params = {
            "starttime": str(starttime),
            "endtime": str(endtime)
        }
        status, res = utils._request("GET", url="/v1/history_econs_calendar", data=params)
        logger.info(f"Successfully fetched upcoming economic calendar")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_history_econs_calendar tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

