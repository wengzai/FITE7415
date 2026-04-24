# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def backtest_run(
    code: str,
    settings: object
) -> Dict[str, Any]:
    try:
        logger.info(f"Starting a backtest")

        params = {
            "code": code,
            "settings": settings
        }
        
        status, res = utils._request("POST", url="/v1/run_backtest", data=params)
        logger.info(f"Successfully start a backtest")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in backtest_run tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

