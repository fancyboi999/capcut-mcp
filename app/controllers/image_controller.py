from fastapi.responses import JSONResponse
from app.schemas import AddImageRequest, ResponseModel
from add_image_impl import add_image_impl

async def add_image(request: AddImageRequest) -> JSONResponse:
    result = ResponseModel()

    # Validate required parameters
    if not request.image_url:
        result.error = "Hi, the required parameters 'image_url' are missing."
        return JSONResponse(content=result.dict())

    try:
        draft_result = add_image_impl(
            draft_folder=request.draft_folder,
            image_url=request.image_url,
            width=request.width,
            height=request.height,
            start=request.start,
            end=request.end,
            draft_id=request.draft_id,
            transform_y=request.transform_y,
            scale_x=request.scale_x,
            scale_y=request.scale_y,
            transform_x=request.transform_x,
            track_name=request.track_name,
            relative_index=request.relative_index,
            animation=request.animation,
            animation_duration=request.animation_duration,
            intro_animation=request.intro_animation,
            intro_animation_duration=request.intro_animation_duration,
            outro_animation=request.outro_animation,
            outro_animation_duration=request.outro_animation_duration,
            combo_animation=request.combo_animation,
            combo_animation_duration=request.combo_animation_duration,
            transition=request.transition,
            transition_duration=request.transition_duration,
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
        result.error = f"Error occurred while processing image: {str(e)}."
        return JSONResponse(content=result.dict()) 