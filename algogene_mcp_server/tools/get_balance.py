# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_balance(
    runmode: str,
    accountid: str,
    token: str
) -> Dict[str, Any]:
    try:
        logger.info(f"Fetching current balance for account: {runmode}-{accountid}")

        params = {
            "runmode": str(runmode),
            "accountid": str(accountid),
            "token": str(token)
        }
        status, res = utils._request("GET", url="/v1/balance", data=params)
        logger.info(f"Successfully fetched current balance for account: {runmode}-{accountid}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_balance tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

