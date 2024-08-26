from typing import Any, Optional

from pydantic import BaseModel


class DefaultResponse(BaseModel):
    status: str = "Failed"
    message: Optional[str]
    data: Optional[Any]


class DefaultFailureResponse(DefaultResponse):
    error: Any


class DefaultSuccessResponse(BaseModel):
    status: str = "success"
    message: Optional[str]
    data: Optional[Any]


class LoadStylesResponse(BaseModel):
    styles: list = []
    js_files: list = []
    assetPath: str = None