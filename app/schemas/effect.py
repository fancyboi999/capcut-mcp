from pydantic import BaseModel
from typing import Optional, List, Any

class AddEffectRequest(BaseModel):
    effect_type: str
    start: Optional[float] = 0
    end: Optional[float] = 3.0
    draft_id: Optional[str] = None
    track_name: Optional[str] = "effect_01"
    params: Optional[List[Any]] = None
    width: Optional[int] = 1080
    height: Optional[int] = 1920

class AddStickerRequest(BaseModel):
    sticker_id: str
    start: Optional[float] = 0
    end: Optional[float] = 5.0
    draft_id: Optional[str] = None
    transform_y: Optional[float] = 0
    transform_x: Optional[float] = 0
    alpha: Optional[float] = 1.0
    flip_horizontal: Optional[bool] = False
    flip_vertical: Optional[bool] = False
    rotation: Optional[float] = 0.0
    scale_x: Optional[float] = 1.0
    scale_y: Optional[float] = 1.0
    track_name: Optional[str] = 'sticker_main'
    relative_index: Optional[int] = 0
    width: Optional[int] = 1080
    height: Optional[int] = 1920 