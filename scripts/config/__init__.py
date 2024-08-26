"""
This file exposes configurations from config file and environments as Class Objects
"""
import shutil

from dotenv import load_dotenv

load_dotenv()
import os.path
import sys
from configparser import BasicInterpolation, ConfigParser
from pydantic import Field, BaseSettings

PROJECT_NAME = "Lambweston Gauge Meter"


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
    config.read("conf/application.conf")
except Exception as e:
    print(f"Error while loading the config: {e}")
    print("Failed to Load Configuration. Exiting!!!")
    sys.stdout.flush()
    sys.exit()


class _Service(BaseSettings):
    HOST = config.get("SERVICE", "host")
    PORT = int(config.get("SERVICE", "port"))
    WORKERS = int(config.get("SERVICE", "workers"))
    verify_signature = config.getboolean("SERVICE", "verify_signature", fallback=True)
    BUILD_DIR: str = Field(default="scripts/templates")
    PLUGIN_NAME: str = Field(default="CustomCoilParameterDashboard")
    PROXY: str = Field(default="/hack-repl")
    BACKEND_DIR: str = Field(default=".")


class _PathToDir(BaseSettings):
    ASSETS: str = Field(default=f"{_Service().BUILD_DIR}/assets")


class DBConf:
    KAIROS_URI = config.get("KAIROS_DETAILS", "kairos_uri")
    KAIROS_USERNAME = config.get("KAIROS_DETAILS", "kairos_username")
    KAIROS_PASSWORD = config.get("KAIROS_DETAILS", "kairos_password")
    KAIROS_METRIC = config.get("KAIROS_DETAILS", "kairos_metric")
    # if not KAIROS_URI:
    #     print("Error, environment variable KAIROS_URI not set")
    #     sys.exit(1)


class PathToStorage:
    BASE_PATH = config.get("DIRECTORY", "base_path")
    if not BASE_PATH:
        print("Error, environment variable BASE_PATH not set")
        sys.exit(1)
    MOUNT_DIR = config.get("DIRECTORY", "mount_dir")
    if not MOUNT_DIR:
        print("Error, environment variable MOUNT_DIR not set")
        sys.exit(1)
    MODULE_PATH = os.path.join(BASE_PATH, MOUNT_DIR)
    FORM_IO_UPLOADS = os.path.join(MODULE_PATH, "form_io_uploads")
    UPLOAD_FILE_PATH = os.path.join(MODULE_PATH, "csv_files")
    LOGS_MODULE_PATH = f"{BASE_PATH}/logs{MOUNT_DIR}/"

class logging_details:
    log_level = config.get("LOG DETAILS", "level", fallback="DEBUG")
    log_level = log_level or "INFO"
    log_base_path = config.get("LOG DETAILS", "log_base_path")
    log_max_bytes = int(config.get("LOG DETAILS", "log_max_byte"))
    handler_type = config.get("LOG DETAILS", "handler_type")
    log_file_name = config.get("LOG DETAILS", "log_file_name")
    backup_count = config.get("LOG DETAILS", "backup_count")


class PathToQa:
    PATH_TO_QA_API = config.get("PATH_TO_QA_API", "qa_base_url")
    if not bool(PATH_TO_QA_API):
        print("PATH_TO_QA_API not found")


Service = _Service()
PathToDir = _PathToDir()
