# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_history_econs_stat(
    series_id: str,
    starttime: str,
    endtime: str
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching economic time series history")

        params = {
            "series_id": str(series_id),
            "starttime": str(starttime),
            "endtime": str(endtime)
        }
        status, res = utils._request("GET", url="/v1/history_econs_stat", data=params)
        logger.info(f"Successfully fetched economic time series history")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_history_econs_stat tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

