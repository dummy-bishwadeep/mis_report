"""
This file exposes configurations from config file and environments as Class Objects
"""

import os.path
import sys
from configparser import BasicInterpolation, ConfigParser

from dotenv import load_dotenv
load_dotenv()

class EnvInterpolation(BasicInterpolation):
    """
    Interpolation which expands environment variables in values.
    """

    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)

        if not os.path.expandvars(value).startswith("$"):
            return os.path.expandvars(value)
        else:
            return

try:
    config = ConfigParser(interpolation=EnvInterpolation())

    current_file_path = os.path.abspath(__file__)
    project_parent_path = current_file_path

    for _ in range(3):
        project_parent_path = os.path.dirname(project_parent_path)
    config_path = os.path.join(project_parent_path, 'conf/application.conf')
    config.read(config_path)
except Exception as e:
    print(f"Error while loading the config: {e}")
    print("Failed to Load Configuration. Exiting!!!")
    sys.stdout.flush()
    sys.exit()


class LoggingDetails:
    LOG_LEVEL: str = config["LOG DETAILS"]["log_level"]
    LOG_BASE_PATH: str = config["LOG DETAILS"]["log_base_path"]
    LOG_MAX_BYTES: int = int(config["LOG DETAILS"]["log_max_byte"])
    HANDLER_TYPE: str = config["LOG DETAILS"]["handler_type"]
    LOG_FILE_NAME: str = config["LOG DETAILS"]["log_file_name"]
    BACKUP_COUNT: int = int(config["LOG DETAILS"]["backup_count"])
    ENABLE_CONSOLE_LOG: bool = True
    TRACEBACK_FLAG: bool = True
    ENABLE_FILE_LOG: bool = True


class Path:
    CONFIG_PATH: str = config["PATH"]["CONFIG_PATH"]


class Service:
    SERVICE_HOST: str = config["SERVICE"]["host"]
    SERVICE_PORT: int = int(config["SERVICE"]["port"])


class DBConf:
    KAIROS_URI = config.get("KAIROS_DETAILS", "kairos_uri")
    KAIROS_USERNAME = config.get("KAIROS_DETAILS", "kairos_username")
    KAIROS_PASSWORD = config.get("KAIROS_DETAILS", "kairos_password")
    KAIROS_METRIC = config.get("KAIROS_DETAILS", "kairos_metric")
