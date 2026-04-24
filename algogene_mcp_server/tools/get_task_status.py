# Original version:
# import logging
# import utils
import logging
from typing import Any, Dict, List
import utils

logger = logging.getLogger(__name__)


def get_task_status(
    task: str,
    task_id: str
) -> Dict[str, Any]:
    try:
        logger.info(f"Query a task status for: {task_id}")

        params = {
            "task": task,
            "task_id": task_id
        }
        status, res = utils._request("GET", url="/v1/task_status", data=params)
        logger.info(f"Successfully fetched task status: {task_id}")
        return res
        
    except Exception as e:
        logger.error(f"Unexpected error in get_task_status tool: {str(e)}")
        return f"Tool execution failed: {str(e)}"

