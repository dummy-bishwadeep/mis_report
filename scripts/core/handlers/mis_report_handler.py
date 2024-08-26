import copy
import json
import os
import shutil
from openpyxl.reader.excel import load_workbook
from openpyxl.styles import PatternFill
from scripts.core.constants import PathConstants
from scripts.core.constants.report_constants import ReportConstants
from scripts.utils.kairos.kairos_connection import KairosDBUtility
# from scripts.logging import logger as logger
from scripts.config import DBConf
import warnings
from openpyxl.drawing.image import Image
from pathlib import Path

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl.reader.drawings")

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
        tags = request_data["tag_ids_list"]
        query = {
            "metrics": [
                {
                    "tags": {
                        "c3": tags
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

    def generate_report(self, data=None):
        try:
            data = ReportConstants.sample_data
            # create output template
            metadata = data.get('metadata', {})
            created_on = metadata.get('created_on', '')
            file_name = f'Mis_Report_{created_on}.xlsx'
            output_file_path = os.path.join(PathConstants.output_template_dir, file_name)
            shutil.copy(PathConstants.template_path, output_file_path)

            # ToDo: Add functionality for report backup count in reports directory
            # ToDo: Add proper loggers

            # Write data to excel
            self.write_data_to_excel(data=data, output_file=output_file_path)
            return file_name, output_file_path
        except Exception as generate_report_error:
            # logger.exception(f"Error while generating report: {generate_report_error}")
            raise generate_report_error

    def write_data_to_excel(self, data, output_file):
        try:
            # Load Workbook
            wb = load_workbook(output_file)
            ws = wb.active

            # Write Mis Report Metadata
            self.write_metadata(data, ws)

            # Start writing from row 13
            start_row = 13

            # Iterate over each division in the data
            for line in data['lines']:
                div = line['div']
                energy_types = line['energy_type']

                # Create fill colors for the division and energy types
                div_fill_color = PatternFill(start_color=line['div_color'].replace('#', ''), fill_type="solid")
                energy_fill_color = PatternFill(start_color=line['energy_color'].replace('#', ''), fill_type="solid")

                # Store the starting row for the division (to merge cells later)
                div_start_row = copy.deepcopy(start_row)

                # Iterate over each energy type within the division
                ws, start_row = self.write_energy_data(ws, energy_types, start_row, energy_fill_color)

                # Merge cells for the division name in column 1 and apply styles
                self.merge_div_column(ws, div_start_row, div_fill_color, div, start_row)

                # Add two extra rows as dividers between divisions
                for _ in range(2):
                    for col in range(1, 4):
                        ws.cell(row=start_row, column=col).fill = PatternFill(start_color='FFFFCC', fill_type="solid")
                    start_row += 1

            # Write the static parameters at the end of the data
            ws, start_row = self.write_static_parameters_data(data, start_row, ws)

            # Apply borders to all relevant cells
            for row in range(13, start_row):
                for col in range(1, 4):
                    ws.cell(row=row, column=col).border = ReportConstants.thin_border

            # insert logo
            self.insert_aym_logo(ws)
            self.insert_kl_logo(ws)

            # Set the width of column A
            ws.column_dimensions['A'].width = 15

            # Save the modified workbook to the destination file
            wb.save(output_file)

        except Exception as report_error:
            # logger.exception(f"Error while processing data for report: {report_error}")
            raise report_error

    @staticmethod
    def write_energy_data(ws, energy_types, start_row, energy_fill_color):
        try:
            for energy in energy_types:
                # Write the energy type label in column 2 and apply styles
                ws.cell(row=start_row, column=2, value=energy['label']).font = ReportConstants.bold_font
                ws.cell(row=start_row, column=2).fill = energy_fill_color
                ws.cell(row=start_row, column=3).fill = energy_fill_color

                # Iterate over the energy data (e.g., Machine, Chiller, etc.)
                for key, value in energy['data'].items():
                    start_row += 1
                    # Write the energy data key in column 2 and apply styles
                    ws.cell(row=start_row, column=2,
                            value=key).font = ReportConstants.red_font if key == "TOTAL" else ReportConstants.bold_font
                    ws.cell(row=start_row, column=2).fill = energy_fill_color

                    # Write the corresponding value in column 3 with styles
                    cell = ws.cell(row=start_row, column=3, value=value)
                    cell.font = ReportConstants.red_font if key == "TOTAL" else ReportConstants.normal_font
                    cell.alignment = ReportConstants.center_align
                    cell.fill = PatternFill(start_color='FFFFFF',
                                            fill_type='solid') if key == "TOTAL" else energy_fill_color

                # Move to the next row for the next energy type
                start_row += 1
            return ws, start_row
        except Exception as energy_error:
            raise energy_error

    @staticmethod
    def write_static_parameters_data(data, start_row, ws):
        try:
            # Write the static parameters
            static_fill_color = PatternFill(start_color=data['static_color'].replace('#', ''), fill_type="solid")
            for key, value in data['static_params'].items():
                # Write the parameter name in column 2 and the value in column 3
                ws.cell(row=start_row, column=2, value=key).font = ReportConstants.bold_font
                ws.cell(row=start_row, column=3).value = value
                ws.cell(row=start_row, column=3).font = ReportConstants.normal_font
                for col in range(1, 4):
                    ws.cell(row=start_row, column=col).fill = static_fill_color
                start_row += 1
            return ws, start_row
        except Exception as xlsx_error:
            # logger.exception(f"Error while writing static parameters data: {xlsx_error}")
            raise xlsx_error

    @staticmethod
    def merge_div_column(ws, div_start_row, div_fill_color, div, start_row):
        try:
            ws.merge_cells(start_row=div_start_row, start_column=1, end_row=start_row - 1, end_column=1)
            div_cell = ws.cell(row=div_start_row, column=1, value=div)
            div_cell.border = ReportConstants.thin_border
            div_cell.alignment = ReportConstants.rotate_text
            div_cell.font = ReportConstants.div_font
            div_cell.fill = div_fill_color
        except Exception as merge_error:
            raise merge_error

    @staticmethod
    def write_metadata(data, ws):
        try:
            metadata = data.get('metadata', {})
            created_by = metadata.get('created_by', '')
            created_on = metadata.get('created_on', '')
            report_date = metadata.get('report_date', '')
            metadata = [created_by, created_on, report_date]

            start_row = 8
            for index in range(0, 3):
                ws.cell(row=start_row, column=3).value = metadata[index]
                ws.cell(row=start_row, column=3).alignment = ReportConstants.center_align
                start_row += 1

        except Exception as metadata_error:
            raise metadata_error

    @staticmethod
    def insert_kl_logo(ws):
        try:
            img_path = Path(PathConstants.kl_logo)
            img = Image(img_path)
            img.anchor = 'C1'

            # Add the image to the worksheet
            ws.add_image(img)
        except Exception as logo_error:
            raise logo_error

    @staticmethod
    def insert_aym_logo(ws):
        try:
            img_path = Path(PathConstants.aym_logo)
            img = Image(img_path)
            img.anchor = 'A2'

            # Add the image to the worksheet
            ws.add_image(img)
        except Exception as logo_error:
            raise logo_error
