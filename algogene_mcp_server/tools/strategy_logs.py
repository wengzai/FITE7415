# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def strategy_logs(
    runmode: str,
    runtime_id: str
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching system logs for account: {runmode}-{runtime_id}")

        params = {
            "runmode": str(runmode),
            "runtime_id": str(runtime_id)
        }
        status, res = utils._request("GET", url="/v1/strategy_logs", data=params)
        logger.info(f"Successfully fetched system logs for account: {runmode}-{runtime_id}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in strategy_logs tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

