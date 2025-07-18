from pydantic import BaseModel
from typing import Optional, Any

class AddAudioRequest(BaseModel):
    draft_folder: Optional[str] = None
    audio_url: str
    start: Optional[float] = 0
    end: Optional[float] = None
    draft_id: Optional[str] = None
    volume: Optional[float] = 1.0
    target_start: Optional[float] = 0
    speed: Optional[float] = 1.0
    track_name: Optional[str] = 'audio_main'
    duration: Optional[float] = None
    effect_type: Optional[str] = None
    effect_params: Optional[Any] = None
    width: Optional[int] = 1080
    height: Optional[int] = 1920 