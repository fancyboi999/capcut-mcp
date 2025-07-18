from fastapi import APIRouter
from app.schemas import AddAudioRequest
from app.controllers import add_audio

router = APIRouter(tags=["音频"])

@router.post('/add_audio',operation_id='add_audio')
async def add_audio_route(request: AddAudioRequest):
    return await add_audio(request) 