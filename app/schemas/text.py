from pydantic import BaseModel
from typing import Optional, Any

class AddTextRequest(BaseModel):
    text: str
    start: float
    end: float
    draft_id: Optional[str] = None
    transform_y: Optional[float] = 0
    transform_x: Optional[float] = 0
    font: Optional[str] = "文轩体"
    font_color: Optional[str] = "#FF0000"
    font_size: Optional[float] = 8.0
    track_name: Optional[str] = "text_main"
    vertical: Optional[bool] = False
    font_alpha: Optional[float] = 1.0
    border_alpha: Optional[float] = 1.0
    border_color: Optional[str] = "#000000"
    border_width: Optional[float] = 0.0
    background_color: Optional[str] = "#000000"
    background_style: Optional[int] = 0
    background_alpha: Optional[float] = 0.0
    bubble_effect_id: Optional[str] = None
    bubble_resource_id: Optional[str] = None
    effect_effect_id: Optional[str] = None
    intro_animation: Optional[str] = None
    intro_duration: Optional[float] = 0.5
    outro_animation: Optional[str] = None
    outro_duration: Optional[float] = 0.5
    width: Optional[int] = 1080
    height: Optional[int] = 1920
    fixed_width: Optional[float] = -1
    fixed_height: Optional[float] = -1

class AddSubtitleRequest(BaseModel):
    srt: str
    draft_id: Optional[str] = None
    time_offset: Optional[float] = 0.0
    font_size: Optional[float] = 5.0
    bold: Optional[bool] = False
    italic: Optional[bool] = False
    underline: Optional[bool] = False
    font_color: Optional[str] = '#FFFFFF'
    vertical: Optional[bool] = False
    alpha: Optional[float] = 1
    border_alpha: Optional[float] = 1.0
    border_color: Optional[str] = '#000000'
    border_width: Optional[float] = 0.0
    background_color: Optional[str] = '#000000'
    background_style: Optional[int] = 0
    background_alpha: Optional[float] = 0.0
    transform_x: Optional[float] = 0.0
    transform_y: Optional[float] = -0.8
    scale_x: Optional[float] = 1.0
    scale_y: Optional[float] = 1.0
    rotation: Optional[float] = 0.0
    track_name: Optional[str] = 'subtitle'
    width: Optional[int] = 1080
    height: Optional[int] = 1920 