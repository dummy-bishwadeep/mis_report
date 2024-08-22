# from scripts.logging import logger as logger
import traceback
from fastapi import APIRouter
from scripts.core.constants.api import APIEndpoints
from scripts.core.handlers.mis_report_handler import MisReport
# from scripts.core.schemas.response_models import (DefaultFailureResponse, DefaultSuccessResponse)

mis_router = APIRouter(prefix=APIEndpoints.widget)


@mis_router.post(APIEndpoints.get_mis_report)
def load_json_data():
    try:
        print("Inside read_mis_data service")
        # logger.debug("Inside read_mis_data service")
        file_path = "D:\AYM\MIS_Report\MIS_Report\MIS_Report\input.json"
        data, tags, tag_dict = MisReport().read_json_file(file_path)
        return tags,tag_dict
    except Exception as e:
        traceback.print_exc()
        # logger.exception(f"Exception while reading pareto data: {e}")
        # return DefaultFailureResponse(error=str(e))

