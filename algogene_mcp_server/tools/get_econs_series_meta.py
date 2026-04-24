# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_econs_series_meta(
    series_id: str
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching meta data for economic time series: {series_id}")

        params = {
            "series_id": str(series_id)
        }
        status, res = utils._request("GET", url="/v1/meta_econs_series", data=params)

        logger.info(f"Successfully fetched economic time series meta data for {series_id}: {res}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_econs_series_meta tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

