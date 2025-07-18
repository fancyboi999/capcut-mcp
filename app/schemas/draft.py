from pydantic import BaseModel
from typing import Optional

class CreateDraftRequest(BaseModel):
    width: Optional[int] = 1080
    height: Optional[int] = 1920

class SaveDraftRequest(BaseModel):
    draft_id: str
    draft_folder: Optional[str] = None

class QueryDraftStatusRequest(BaseModel):
    task_id: str

class GenerateDraftUrlRequest(BaseModel):
    draft_id: str
    draft_folder: Optional[str] = None

class QueryScriptRequest(BaseModel):
    draft_id: str
    force_update: Optional[bool] = True 