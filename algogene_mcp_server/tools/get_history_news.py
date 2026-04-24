# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_history_news(
    lang: str,
    count: int,
    starttime: str,
    endtime: str,
    category: str = "",
    source: str = ""
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching historical news: {lang} {category} {source}")

        params = {
            "count": int(count),
            "lang": str(lang),
            "starttime": str(starttime),
            "endtime": str(endtime),
            "category": str(category),
            "source": str(source)
        }
        status, res = utils._request("GET", url="/v1/history_news", data=params)
        logger.info(f"Successfully fetched historical news for {lang} {category} {source}: {res}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_history_news tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

