# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def strategy_trade(
    runmode: str,
    runtime_id: str,
    acdate: str,
    orderRef: str = ""
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching transaction history for account: {runmode}-{runtime_id}")

        params = {
            "runmode": str(runmode),
            "runtime_id": str(runtime_id),
            "acdate": str(acdate)
        }
        if orderRef!="": params['orderRef'] = str(orderRef) 

        status, res = utils._request("GET", url="/v1/strategy_trade", data=params)
        logger.info(f"Successfully fetched transaction history for account: {runmode}-{runtime_id}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in strategy_trade tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

