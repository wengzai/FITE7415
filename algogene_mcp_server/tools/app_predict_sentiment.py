# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def app_predict_sentiment(
    sentences: List[str],
) -> Dict[str, Any]:
    try:
        logger.info(f"Running app_predict_sentiment")

        params = {
            "sentences": sentences if type(sentences)==list else [sentences]
        }
        status, res = utils._request_app("POST", url="/v1/bot/4/main.predict_sentiment", data=params)
        logger.info(f"Successfully run app_predict_sentiment")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in app_predict_sentiment tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

