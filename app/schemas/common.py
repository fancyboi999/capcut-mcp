from pydantic import BaseModel
from typing import Optional, Any

class ResponseModel(BaseModel):
    success: bool = False
    output: Any = ""
    error: str = "" 