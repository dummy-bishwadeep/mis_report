import json
from scripts.logging import logger as logger
import traceback
from fastapi import APIRouter
from scripts.core.constants.api import APIEndpoints
from scripts.core.handlers.mis_report_handler import MisReport
from scripts.core.schemas.request_model import MisModel
from scripts.core.schemas.response_models import (DefaultFailureResponse, DefaultSuccessResponse)
import os.path
from starlette.responses import FileResponse
from scripts.core.constants import PathConstants
mis_router = APIRouter(prefix=APIEndpoints.widget)


@mis_router.post(APIEndpoints.get_mis_report)
def load_json_data(input_json: MisModel):
    try:

        logger.debug("Inside read_mis_data service")
        file_path = os.path.join(PathConstants.project_directory, 'input.json')
        edit_file_path = os.path.join(PathConstants.project_directory, 'output.json')
        data, tags, tag_dict = MisReport().read_json_file(input_json.dict())
        if data:
            # Write the input JSON to a new file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        request_data = dict()
        if data and tags:
            request_data["tag_ids_list"] = tags
            request_data["start_date"] = data["start_date"]
            request_data["end_date"] = data["end_date"]
            request_data["tz"] = data["tz"]
            kairos_response = MisReport().fetch_kairos_data(request_data)
            if not kairos_response["status"]:
                # tag_id_values = MisReport().get_tag_values(kairos_response)
                tag_id_values={'tag_1':'10','tag_2':'20','tag_3':'30','tag_4':'40','tag_5':'50','tag_6':'60','tag_7':'70','tag_8':'80','tag_9':'90','tag_10':'100','tag_11':'110','tag_12':'120','tag_13':'130','tag_14':'140','tag_15':'150','tag_16':'160','tag_17':'170','tag_18':'180','tag_19':'190','tag_20':'200','tag_21':'210','tag_22':'220','tag_23':'230','tag_24':'240'}
                if tag_id_values:
                    MisReport().update_json_file(file_path,tag_id_values,edit_file_path)
                final_json = MisReport().create_final_output_json(edit_file_path)

                file_name, file_path = MisReport().generate_report(final_json)
                if os.path.exists(file_path):
                    return final_json
                    # return FileResponse(file_path,
                    #     headers={"Content-Disposition": f"attachment; filename={file_name}"},
                    #     media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        traceback.print_exc()
        logger.exception(f"Exception while reading pareto data: {e}")

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