from pydantic import BaseModel
from typing import Optional, Any

class AddVideoRequest(BaseModel):
    draft_folder: Optional[str] = None
    video_url: str
    start: Optional[float] = 0
    end: Optional[float] = 0
    width: Optional[int] = 1080
    height: Optional[int] = 1920
    draft_id: Optional[str] = None
    transform_y: Optional[float] = 0
    scale_x: Optional[float] = 1
    scale_y: Optional[float] = 1
    transform_x: Optional[float] = 0
    speed: Optional[float] = 1.0
    target_start: Optional[float] = 0
    track_name: Optional[str] = "video_main"
    relative_index: Optional[int] = 0
    duration: Optional[float] = None
    transition: Optional[str] = None
    transition_duration: Optional[float] = 0.5
    volume: Optional[float] = 1.0
    mask_type: Optional[str] = None
    mask_center_x: Optional[float] = 0.5
    mask_center_y: Optional[float] = 0.5
    mask_size: Optional[float] = 1.0
    mask_rotation: Optional[float] = 0.0
    mask_feather: Optional[float] = 0.0
    mask_invert: Optional[bool] = False
    mask_rect_width: Optional[float] = None
    mask_round_corner: Optional[float] = None

class AddVideoKeyframeRequest(BaseModel):
    draft_id: Optional[str] = None
    track_name: Optional[str] = 'video_main'
    property_type: Optional[str] = 'alpha'
    time: Optional[float] = 0.0
    value: Optional[str] = '1.0'
    property_types: Optional[list] = None
    times: Optional[list] = None
    values: Optional[list] = None 