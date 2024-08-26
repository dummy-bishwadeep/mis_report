# from scripts.logging import logger as logger
import os.path
import traceback
from fastapi import APIRouter
from starlette.responses import FileResponse

from scripts.core.constants.api import APIEndpoints
from scripts.core.handlers.mis_report_handler import MisReport
# from scripts.core.schemas.response_models import (DefaultFailureResponse, DefaultSuccessResponse)

mis_router = APIRouter(prefix=APIEndpoints.widget)


@mis_router.post(APIEndpoints.get_mis_report)
def load_json_data():
    try:
        print("Inside read_mis_data service")
        # logger.debug("Inside read_mis_data service")
        file_path = "D:\AYM\MIS_Report\MIS_Report\input.json"
        data, tags, tag_dict = MisReport().read_json_file(file_path)
        return tags,tag_dict
        # return DefaultSuccessResponse(message="Widgets Fetched Successfully", data=data)
    except Exception as e:
        traceback.print_exc()
        # logger.exception(f"Exception while reading pareto data: {e}")
        # return DefaultFailureResponse(error=str(e))


@mis_router.post(APIEndpoints.generate_report)
def generate_mis_report():
    try:
        mis_report_handler = MisReport()
        file_name, file_path = mis_report_handler.generate_report()
        if os.path.exists(file_path):
            return FileResponse(file_path,
                                headers={"Content-Disposition": f"attachment; filename={file_name}"},
                                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as report_error:
        traceback.print_exc()
        raise report_error
