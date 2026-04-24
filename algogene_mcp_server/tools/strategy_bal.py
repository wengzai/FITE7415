# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def strategy_bal(
    runmode: str,
    runtime_id: str,
    acdate: str = ""
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching account balance history for account: {runmode}-{runtime_id}")

        params = {
            "runmode": str(runmode),
            "runtime_id": str(runtime_id)
        }
        if acdate!="": params['acdate'] = str(acdate) 

        status, res = utils._request("GET", url="/v1/strategy_bal", data=params)
        logger.info(f"Successfully fetched account balance history for account: {runmode}-{runtime_id}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in strategy_bal tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

