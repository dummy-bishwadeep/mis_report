import json
from scripts.utils.kairos.kairos_connection import KairosDBUtility
# from scripts.logging import logger as logger
from scripts.config.app_configurations import DBConf
# from scripts.core.constants import constants


class MisReport:
    def __init__(self, project_id=None):
        # self.project_id = project_id
        self.kairos_obj = KairosDBUtility(base_url=DBConf.KAIROS_URI, username=DBConf.KAIROS_USERNAME,
                                          password=DBConf.KAIROS_PASSWORD)

    def read_json_file(self,file_path):
        """
        Reads and parses a JSON file.

        Parameters:
        - file_path (str): The path to the JSON file.

        Returns:
        - dict: The JSON content as a Python dictionary.
        """
        tag_ids_list = list()
        tags_dict = dict()
        try:
            with open(file_path, 'r') as file:
                # Load JSON data from the file
                data = json.load(file)
                if data:
                    for each_key in data:
                        if each_key == "static_params":
                            for each_static_parameter in data[each_key]:
                                # for each_tag in data[each_key][each_static_parameter]:
                                tag_ids_list.append(data[each_key][each_static_parameter])
                                tags_dict[each_static_parameter] = data[each_key][each_static_parameter]

                        if each_key == "lines":
                            for line_category in data[each_key]:
                                for each_line in data[each_key][line_category]:
                                    for each_param in data[each_key][line_category][each_line]:
                                        for each_tag in data[each_key][line_category][each_line][each_param]:
                                            if each_tag not in ("meter_position","constant"):
                                                tag_ids_list.append(data[each_key][line_category][each_line][each_param][each_tag])
                                                tags_dict[each_line + "_" + each_tag] = data[each_key][line_category][each_line][each_param][each_tag]




                    return data, tag_ids_list, tags_dict
        except FileNotFoundError:
            print(f"Error: The file at path '{file_path}' was not found.")
            return None, tag_ids_list, tags_dict
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the file.")
            return None, tag_ids_list, tags_dict
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None, tag_ids_list, tags_dict

    def fetch_kairos_data(self, request_data):
        """
        This method is to get the kairos data
        :param request_data:
        :return:
        """
        response_json = dict(
            status=False,
            message="No data within the selected date range",
            data=[]
        )
        query = {
            "metrics": [
                {
                    "tags": {
                        "c3": request_data.kairos_tag
                    },
                    "name": DBConf.KAIROS_METRIC,
                    "group_by": [
                        {
                            "name": "tag",
                            "tags": [
                                "C3"
                            ]
                        }
                    ],
                    "aggregators": [
                        {
                            "name": "sum",
                            "sampling": {
                                "value": "1",
                                "unit": "days"
                            },
                            "align_sampling": True,
                            "align_start_time": True
                        }
                    ]
                }
            ],
            "plugins": [],
            "cache_time": 0,
            "time_zone": request_data.tz,
            "start_absolute": self.convert_datetime_to_epoch(date_time=request_data.start_date),
            "end_absolute": self.convert_datetime_to_epoch(date_time=request_data.end_date)
        }
        # logger.info(f"Kairos Query: {query}")
        try:
            kairos_response = self.kairos_obj.read(query)

            if kairos_response["queries"][0]["results"][0]["values"]:
                for each_data in kairos_response["queries"][0]["results"][0]["values"]:
                    each_data[0] = self.convert_epoch_to_datetime(epoch_time=each_data[0])

                response_json = dict(
                    status=True,
                    message="Data fetched successfully",
                    data=kairos_response["queries"][0]["results"][0]["values"]
                )
        except Exception as e:
            # logger.exception("Exception when loading the data in pareto chart")
            raise e
        return response_json







