# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def search_econs_series(
    titles: str,
    freq: str = "",
    geo: str = ""
) -> Dict[str, Any]:
    try:
        logger.info(f"Searching economic time series")

        params = {
            "titles": str(titles)
        }
        if freq!="":
            params['freq'] = str(freq)
        if geo!="":
            params['geo'] = str(geo)

        status, res = utils._request("GET", url="/v1/search_econs_series", data=params)
        logger.info(f"Successfully fetched related economic time series")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in search_econs_series tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

