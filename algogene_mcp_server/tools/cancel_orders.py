# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def cancel_orders(
    runmode: str,
    accountid: str,
    token: str,
    tradeIDs: str
) -> Dict[str, Any]:
    try:
        logger.info(f"Cancelling pending order(s) for account: {runmode}-{accountid}")

        params = {
            "runmode": str(runmode),
            "accountid": str(accountid),
            "token": str(token),
            "tradeIDs": str(tradeIDs)
        }
        
        status, res = utils._request("POST", url="/v1/cancel_orders", data=params)
        logger.info(f"Successfully cancel order(s) for account: {runmode}-{accountid}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in cancel_orders tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

