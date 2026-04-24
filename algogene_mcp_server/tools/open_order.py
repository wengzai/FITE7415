# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def open_order(
    runmode: str,
    accountid: str,
    token: str,
    instrument: str,
    buysell: int,
    volume: float,
    ordertype: str,
    price: float = 0,
    timeinforce: int = 0,
    takeProfitLevel: float = 0,
    stopLossLevel: float = 0,
    holdtime: int = 0,
    orderRef: str = "",
    callback: str = "",
    expiry: str = "",
    right: str = "",
    strike: float = 0,
) -> Dict[str, Any]:
    try:
        logger.info(f"Placing an order for account: {runmode}-{accountid}")

        params = {
            "runmode": str(runmode),
            "accountid": str(accountid),
            "token": str(token),
            "instrument": str(instrument),
            "buysell": str(buysell),
            "volume": float(volume),
            "ordertype": str(ordertype),
        }
        if price!=0: params['price'] = float(price)
        if timeinforce!=0: params['timeinforce'] = int(timeinforce)
        if takeProfitLevel!=0: params['takeProfitLevel'] = float(takeProfitLevel)
        if stopLossLevel!=0: params['stopLossLevel'] = float(stopLossLevel)
        if holdtime!=0: params['holdtime'] = int(holdtime)
        if orderRef!="": params['orderRef'] = str(orderRef)
        if callback!="": params['callback'] = str(callback)
        if expiry!="": params['expiry'] = str(expiry)
        if right!="": params['right'] = str(right)
        if strike!=0: params['strike'] = float(strike)

        status, res = utils._request("POST", url="/v1/open_order", data=params)
        logger.info(f"Successfully place an order for account: {runmode}-{accountid}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in open_order tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

