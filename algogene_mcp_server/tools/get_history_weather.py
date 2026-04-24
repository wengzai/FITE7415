# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_history_weather(
    city: str,
    starttime: str,
    endtime: str
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching weather history for city: {city}")

        params = {
            "city": str(city),
            "starttime": str(starttime),
            "endtime": str(endtime)
        }
        status, res = utils._request("GET", url="/v1/history_weather", data=params)
        logger.info(f"Successfully fetched weather history for city: {city}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_history_weather tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

