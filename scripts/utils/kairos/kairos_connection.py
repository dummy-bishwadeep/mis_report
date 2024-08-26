import requests
import json
from requests.auth import HTTPBasicAuth


class KairosDBUtility:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(username, password)

    def _send_request(self, endpoint, method, data=None):
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        response = requests.request(method, url, headers=headers, data=json.dumps(data) if data else None,
                                    auth=self.auth)

        if response.status_code in [200, 201]:
            return response.json()
        else:
            response.raise_for_status()

    def read(self, query_json):
        """
        Reads data from KairosDB.

        :param query_json: JSON object containing the query
        :return: JSON object with the data or status
        """
        endpoint = 'api/v1/datapoints/query'  # Adjust as necessary
        return self._send_request(endpoint, 'POST', query_json)

    def write(self, data_json):
        """
        Writes data to KairosDB.

        :param data_json: JSON object containing the data to be written
        :return: JSON object with the status or response
        """
        endpoint = 'api/v1/datapoints'  # Adjust as necessary
        return self._send_request(endpoint, 'POST', data_json)

    def delete(self, delete_json):
        """
        Deletes data from KairosDB.

        :param delete_json: JSON object containing the deletion criteria
        :return: JSON object with the status or response
        """
        endpoint = 'api/v1/datapoints/delete'  # Adjust if necessary
        return self._send_request(endpoint, 'POST', delete_json)

#
# # Example usage:
# if __name__ == "__main__":
#     # Replace with your KairosDB base URL, username, and password
#     kairos_db_url = "https://staging.unifytwin.com/kairos/"
#     username = "user name"
#     password = "passwird"
#
#     kairos_db_util = KairosDBUtility(kairos_db_url, username, password)
#
#     # Example read query
#     query = {
#               "metrics": [
#                 {
#                   "tags": {
#                     "c3": [
#                       "l1_100$l2_101$l3_102$l4_103$l5_104$a_123$tag_121"
#                     ]
#                   },
#                   "name": "project_490__ilens.live_data.raw",
#                   "group_by": [
#                     {
#                       "name": "tag",
#                       "tags": [
#                         "C3"
#                       ]
#                     }
#                   ],
#                   "aggregators": [
#                     {
#                       "name": "sum",
#                       "sampling": {
#                         "value": "1",
#                         "unit": "days"
#                       },
#                       "align_sampling": True,
#                       "align_start_time": True
#                     }
#                   ]
#                 }
#               ],
#               "plugins": [],
#               "cache_time": 0,
#               "time_zone": "Asia/Calcutta",
#               "start_absolute": 1719772200000,
#               "end_absolute": 1722969000000
#             }
#
#     try:
#         result = kairos_db_util.read(query)
#         print("Read Result:", result)
#     except Exception as e:
#         print("Error reading data:", e)