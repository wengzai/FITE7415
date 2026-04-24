# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def app_algo_generator(
    prompt: str,
    model: str = ""
) -> Dict[str, Any]:
    try:
        logger.info(f"Running app_algo_generator")

        params = {
            "prompt": prompt
        }
        if model!="": params['model'] = model

        status, res = utils._request_app("POST", url="/v1/bot/127/algo.generate", data=params)
        logger.info(f"Successfully run app_algo_generator")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in app_algo_generator tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

