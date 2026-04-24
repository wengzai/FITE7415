# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_positions(
    runmode: str,
    accountid: str,
    token: str
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching outstanding positions for account: {runmode}-{accountid}")

        params = {
            "runmode": str(runmode),
            "accountid": str(accountid),
            "token": str(token)
        }
        status, res = utils._request("GET", url="/v1/positions", data=params)
        logger.info(f"Successfully fetched outstanding positions for account: {runmode}-{accountid}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_positions tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

