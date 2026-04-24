# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_realtime_econs_calendar(
    count: int
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching upcoming economic calendar")

        params = {
            "count": int(count)
        }
        status, res = utils._request("GET", url="/v1/realtime_econs_calendar", data=params)
        logger.info(f"Successfully fetched upcoming economic calendar")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_realtime_econs_calendar tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

