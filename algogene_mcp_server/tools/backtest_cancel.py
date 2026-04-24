# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def backtest_cancel(
    task_id: str
) -> Dict[str, Any]:
    try:
        logger.info(f"Cancelling a backtest")

        params = {
            "task_id": task_id
        }
        status, res = utils._request("POST", url="/v1/cancel_backtest", data=params)
        logger.info(f"Successfully cancel a backtest")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in backtest_cancel tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

