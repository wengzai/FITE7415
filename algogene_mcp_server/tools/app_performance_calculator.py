# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def app_performance_calculator(
    arr: list[str],
    benchmark: str = ""
) -> Dict[str, Any]:
    try:
        logger.info(f"Running app_performance_calculator")

        params = {
            "arr": arr
        }
        if benchmark!="": params['benchmark'] = benchmark

        status, res = utils._request_app("POST", url="/v1/bot/126/performance.evaluate", data=params)
        logger.info(f"Successfully run app_performance_calculator")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in app_performance_calculator tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

