# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_session() -> Dict[str, Any]:
    try:
        logger.info(f"Fetching session token")

        params = {}
        status, res = utils._request("GET", url="/v1/session", data=params)
        logger.info(f"Successfully fetched session token")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_session tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

