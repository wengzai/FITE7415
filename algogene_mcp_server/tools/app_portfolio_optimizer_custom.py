# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def app_portfolio_optimizer_custom(
    StartDate: str,
    EndDate: str,
    arrUserdata: dict, 
    objective: int,
    basecur: str,
    total_portfolio_value: float = 1000000,
    risk_free_rate: float = 0,
    target_return: float = 0,
    risk_tolerance: float = 0,
    allowShortSell: bool = False,
    group_cond: object = {}
) -> Dict[str, Any]:
    try:
        logger.info(f"Running app_portfolio_optimizer_custom")

        params = {
            "StartDate": str(StartDate),
            "EndDate": str(EndDate),
            "arrUserdata": arrUserdata, 
            "objective": objective,
            "basecur": basecur,
            "total_portfolio_value": total_portfolio_value,
            "risk_free_rate": risk_free_rate,
            "allowShortSell": allowShortSell
        }
        if target_return!=0: params['target_return'] = target_return
        if risk_tolerance!=0: params['risk_tolerance'] = risk_tolerance
        if len(group_cond)>0: params['group_cond'] = group_cond

        status, res = utils._request_app("POST", url="/v1/bot/113/asset.optimize", data=params)
        logger.info(f"Successfully run app_portfolio_optimizer_custom")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in app_portfolio_optimizer_custom tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

