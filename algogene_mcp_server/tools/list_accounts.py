# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def list_accounts(
    runmode: str,
    token: str
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching trading accounts")

        params = {
            "runmode": str(runmode),
            "token": str(token)
        }
        status, res = utils._request("GET", url="/v1/accounts", data=params)
        logger.info(f"Successfully fetched trading accounts")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in list_accounts tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

