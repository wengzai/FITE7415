# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_realtime_weather(
    city: str
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching latest weather for city: {city}")

        params = {
            "city": str(city)
        }
        status, res = utils._request("GET", url="/v1/realtime_weather", data=params)
        logger.info(f"Successfully fetched weather for city: {city}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_realtime_weather tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

