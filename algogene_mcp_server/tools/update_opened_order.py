# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def update_opened_order(
    runmode: str,
    accountid: str,
    token: str,
    tradeID: str,
    takeProfitLevel: float = 0,
    stopLossLevel: float = 0,
    holdtime: int = 0,
    orderRef: str = "",
    callback: str = ""
) -> Dict[str, Any]:
    try:
        logger.info(f"Updateing an opened order for account: {runmode}-{accountid}")

        params = {
            "runmode": str(runmode),
            "accountid": str(accountid),
            "token": str(token),
            "tradeID": str(tradeID)
        }
        if takeProfitLevel!=0: params['takeProfitLevel'] = float(takeProfitLevel)
        if stopLossLevel!=0: params['stopLossLevel'] = float(stopLossLevel)
        if holdtime!=0: params['holdtime'] = int(holdtime)
        if orderRef!="": params['orderRef'] = str(orderRef)
        if callback!="": params['callback'] = str(callback)

        status, res = utils._request("POST", url="/v1/update_opened_order", data=params)
        logger.info(f"Successfully update an opened order for account: {runmode}-{accountid}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in update_opened_order tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

