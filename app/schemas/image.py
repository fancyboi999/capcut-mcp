from pydantic import BaseModel
from typing import Optional

class AddImageRequest(BaseModel):
    draft_folder: Optional[str] = None
    image_url: str
    width: Optional[int] = 1080
    height: Optional[int] = 1920
    start: Optional[float] = 0
    end: Optional[float] = 3.0
    draft_id: Optional[str] = None
    transform_y: Optional[float] = 0
    scale_x: Optional[float] = 1
    scale_y: Optional[float] = 1
    transform_x: Optional[float] = 0
    track_name: Optional[str] = "image_main"
    relative_index: Optional[int] = 0
    animation: Optional[str] = None
    animation_duration: Optional[float] = 0.5
    intro_animation: Optional[str] = None
    intro_animation_duration: Optional[float] = 0.5
    outro_animation: Optional[str] = None
    outro_animation_duration: Optional[float] = 0.5
    combo_animation: Optional[str] = None
    combo_animation_duration: Optional[float] = 0.5
    transition: Optional[str] = None
    transition_duration: Optional[float] = 0.5
    mask_type: Optional[str] = None
    mask_center_x: Optional[float] = 0.0
    mask_center_y: Optional[float] = 0.0
    mask_size: Optional[float] = 0.5
    mask_rotation: Optional[float] = 0.0
    mask_feather: Optional[float] = 0.0
    mask_invert: Optional[bool] = False
    mask_rect_width: Optional[float] = None
    mask_round_corner: Optional[float] = None 