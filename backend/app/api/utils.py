"""
API工具函数
"""

from typing import Any, Dict, List, Optional, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi import status


class ResponseModel(BaseModel):
    """统一API响应模型"""
    code: int
    message: str
    data: Optional[Any] = None


def success_response(
    data: Optional[Any] = None,
    message: str = "操作成功",
    code: int = status.HTTP_200_OK
) -> Dict[str, Any]:
    """
    成功响应
    """
    return {
        "code": code,
        "message": message,
        "data": jsonable_encoder(data) if data is not None else None
    }


def error_response(
    message: str = "操作失败",
    code: int = status.HTTP_400_BAD_REQUEST,
    data: Optional[Any] = None
) -> Dict[str, Any]:
    """
    错误响应
    """
    return {
        "code": code,
        "message": message,
        "data": jsonable_encoder(data) if data is not None else None
    } 