# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_instrument_meta(
    instrument: str
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching contract spec for instrument: {instrument}")

        params = {
            "instrument": str(instrument)
        }
        status, res = utils._request("GET", url="/v1/meta_instrument", data=params)

        logger.info(f"Successfully fetched contract spec for {instrument}: {res}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_instrument_meta tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

