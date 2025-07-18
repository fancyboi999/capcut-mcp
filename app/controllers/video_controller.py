from fastapi.responses import JSONResponse
from app.schemas import AddVideoRequest, AddVideoKeyframeRequest, ResponseModel
from add_video_track import add_video_track
from add_video_keyframe_impl import add_video_keyframe_impl

async def add_video(request: AddVideoRequest) -> JSONResponse:
    result = ResponseModel()

    if not request.video_url:
        result.error = "Hi, the required parameters 'video_url' are missing."
        return JSONResponse(content=result.dict())

    try:
        draft_result = add_video_track(
            draft_folder=request.draft_folder,
            video_url=request.video_url,
            width=request.width,
            height=request.height,
            start=request.start,
            end=request.end,
            target_start=request.target_start,
            draft_id=request.draft_id,
            transform_y=request.transform_y,
            scale_x=request.scale_x,
            scale_y=request.scale_y,
            transform_x=request.transform_x,
            speed=request.speed,
            track_name=request.track_name,
            relative_index=request.relative_index,
            duration=request.duration,
            transition=request.transition,
            transition_duration=request.transition_duration,
            volume=request.volume,
            mask_type=request.mask_type,
            mask_center_x=request.mask_center_x,
            mask_center_y=request.mask_center_y,
            mask_size=request.mask_size,
            mask_rotation=request.mask_rotation,
            mask_feather=request.mask_feather,
            mask_invert=request.mask_invert,
            mask_rect_width=request.mask_rect_width,
            mask_round_corner=request.mask_round_corner
        )
        
        result.success = True
        result.output = draft_result
        return JSONResponse(content=result.dict())

    except Exception as e:
        result.error = f"Error occurred while processing video: {str(e)}."
        return JSONResponse(content=result.dict())

async def add_video_keyframe(request: AddVideoKeyframeRequest) -> JSONResponse:
    result = ResponseModel()

    try:
        draft_result = add_video_keyframe_impl(
            draft_id=request.draft_id,
            track_name=request.track_name,
            property_type=request.property_type,
            time=request.time,
            value=request.value,
            property_types=request.property_types,
            times=request.times,
            values=request.values
        )
        
        result.success = True
        result.output = draft_result
        return JSONResponse(content=result.dict())

    except Exception as e:
        result.error = f"Error occurred while adding keyframe: {str(e)}."
        return JSONResponse(content=result.dict()) 