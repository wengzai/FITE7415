# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def close_orders(
    runmode: str,
    accountid: str,
    token: str,
    tradeIDs: str = "",
    orderRef: str = ""
) -> Dict[str, Any]:
    try:
        logger.info(f"Closing order(s) for account: {runmode}-{accountid}")

        params = {
            "runmode": str(runmode),
            "accountid": str(accountid),
            "token": str(token)
        }
        if tradeIDs!="": params['tradeIDs'] = str(tradeIDs)
        if orderRef!="": params['orderRef'] = str(orderRef)
        
        status, res = utils._request("POST", url="/v1/close_orders", data=params)
        logger.info(f"Successfully close order(s) for account: {runmode}-{accountid}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in close_orders tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

