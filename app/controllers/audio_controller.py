from fastapi.responses import JSONResponse
from app.schemas import AddAudioRequest, ResponseModel
from add_audio_track import add_audio_track

async def add_audio(request: AddAudioRequest) -> JSONResponse:
    result = ResponseModel()

    # If there are audio effect parameters, combine them into sound_effects format
    sound_effects = None
    if request.effect_type is not None:
        sound_effects = [(request.effect_type, request.effect_params)]

    # Validate required parameters
    if not request.audio_url:
        result.error = "Hi, the required parameters 'audio_url' are missing."
        return JSONResponse(content=result.dict())

    try:
        # Call the modified add_audio_track method
        draft_result = add_audio_track(
            draft_folder=request.draft_folder,
            audio_url=request.audio_url,
            start=request.start,
            end=request.end,
            target_start=request.target_start,
            draft_id=request.draft_id,
            volume=request.volume,
            track_name=request.track_name,
            speed=request.speed,
            sound_effects=sound_effects,  # Add audio effect parameters
            width=request.width,
            height=request.height,
            duration=request.duration  # Add duration parameter
        )
        
        result.success = True
        result.output = draft_result
        return JSONResponse(content=result.dict())

    except Exception as e:
        result.error = f"Error occurred while processing audio: {str(e)}."
        return JSONResponse(content=result.dict()) 