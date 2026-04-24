# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_opened_trades(
    runmode: str,
    accountid: str,
    token: str
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching opened trades for account: {runmode}-{accountid}")

        params = {
            "runmode": str(runmode),
            "accountid": str(accountid),
            "token": str(token)
        }
        status, res = utils._request("GET", url="/v1/opened_trades", data=params)
        logger.info(f"Successfully fetched opened trades for account: {runmode}-{accountid}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_opened_trades tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

