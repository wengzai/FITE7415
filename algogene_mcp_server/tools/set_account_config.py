# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def set_account_config(
    runmode: str,
    accountid: str,
    broker_name: str,
    broker_api: str = "",
    broker_account: str = "",
    broker_user: str = "",
    broker_pwd: str = "",
    broker_server: str = "",
    broker_passphrase: str = ""
) -> Dict[str, Any]:
    try:
        logger.info(f"Setup trading account connection: {runmode}-{accountid}")

        params = {
            "runmode": str(runmode),
            "accountid": str(accountid),
            "broker_name": str(broker_name)
        }
        if broker_name in ["aftx", "exness", "tickmill", "fpmarkets", "icmarkets", "roboforex", "pepperstone", "gomarkets", "xmglobal"]:
            params['broker_user'] = str(broker_user)
            params['broker_pwd'] = str(broker_pwd)
            params['broker_server'] = str(broker_server)
        elif broker_name in ["oanda"]:
            params['broker_api'] = str(broker_api)
            params['broker_account'] = str(broker_account)
        elif broker_name in ["ig"]:
            params['broker_api'] = str(broker_api)
            params['broker_account'] = str(broker_account)
            params['broker_user'] = str(broker_user)
            params['broker_pwd'] = str(broker_pwd)
        elif broker_name in ["alpaca", "binance", "bitget", "bybit", "whalefin", "coinex", "bingx", "bitrue"]:
            params['broker_api'] = str(broker_api)
            params['broker_pwd'] = str(broker_pwd)
        elif broker_name in ["okx", "kucoin", "bitmart"]:
            params['broker_api'] = str(broker_api)
            params['broker_pwd'] = str(broker_pwd)
            params['broker_passphrase'] = str(broker_passphrase)
        elif broker_name in ["tigerbrokers", "hyperliquid"]:
            params['broker_api'] = str(broker_api)
            params['broker_account'] = str(broker_account)
            params['broker_pwd'] = str(broker_pwd)
        status, res = utils._request("POST", url="/v1/config", data=params)
        logger.info(f"Successfully setup trading account connection: {runmode}-{accountid}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in set_account_config tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

