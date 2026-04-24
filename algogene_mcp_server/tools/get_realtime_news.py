# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_realtime_news(
    lang: str,
    category: str = "",
    source: str = ""
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching latest news: {lang} {category} {source}")

        params = {
            "lang": str(lang),
            "category": str(category),
            "source": str(source)
        }
        status, res = utils._request("GET", url="/v1/realtime_news", data=params)
        logger.info(f"Successfully fetched latest news for {lang} {category} {source}: {res}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_realtime_news tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

