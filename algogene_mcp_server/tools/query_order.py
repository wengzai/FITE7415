# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def query_order(
    runmode: str,
    accountid: str,
    token: str,
    tradeID: str
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching details of an order for account: {runmode}-{accountid}")

        params = {
            "runmode": str(runmode),
            "accountid": str(accountid),
            "token": str(token),
            "tradeID": str(tradeID)
        }
        status, res = utils._request("GET", url="/v1/query_order", data=params)
        logger.info(f"Successfully fetched details of an order for account: {runmode}-{accountid}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in query_order tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

