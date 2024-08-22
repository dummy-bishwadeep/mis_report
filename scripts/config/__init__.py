from pydantic import Field
from pydantic_settings import BaseSettings

from scripts.config.app_configurations import Service, Path, LoggingDetails


class _Services(BaseSettings):
    HOST: str = Field(default=Service.SERVICE_HOST, env="SERVICE_HOST")
    PORT: int = Field(default=int(Service.SERVICE_PORT), env="SERVICE_PORT")
    ENABLE_CORS: bool = True
    CORS_URLS: list = ["*.ilens.io"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list = ["GET", "POST"]
    CORS_ALLOW_HEADERS: list = ["*"]
    LOG_LEVEL: str = LoggingDetails.LOG_LEVEL
    BACKUP_COUNT: int = LoggingDetails.BACKUP_COUNT
    MAX_BYTES: int = LoggingDetails.LOG_MAX_BYTES
    ENABLE_FILE_LOGGING: bool = True
    # ENABLE_BACKUP_STORING: bool = Field(default=False, env="enable_backup")
    WORKERS: int = Field(default=1, env="workers")


class _BasePathConf(BaseSettings):
    BASE_PATH: str = "/"


class _LoggingDetailsConf(BaseSettings):
    log_level: str = LoggingDetails.LOG_LEVEL
    log_base_path: str = LoggingDetails.LOG_BASE_PATH
    log_max_bytes: int = LoggingDetails.LOG_MAX_BYTES
    handler_type: str = LoggingDetails.HANDLER_TYPE
    log_file_name: str = LoggingDetails.LOG_FILE_NAME
    backup_count: str = LoggingDetails.BACKUP_COUNT


Services = _Services()
logging_details = _LoggingDetailsConf()

__all__ = [
    "Services",
    "logging_details",
]
