from fastapi.responses import JSONResponse
from app.schemas import AddEffectRequest, AddStickerRequest, ResponseModel
from add_effect_impl import add_effect_impl
from add_sticker_impl import add_sticker_impl

async def add_effect(request: AddEffectRequest) -> JSONResponse:
    result = ResponseModel()

    # Validate required parameters
    if not request.effect_type:
        result.error = "Hi, the required parameters 'effect_type' are missing. Please add them and try again."
        return JSONResponse(content=result.dict())

    try:
        # Call add_effect_impl method
        draft_result = add_effect_impl(
            effect_type=request.effect_type,
            start=request.start,
            end=request.end,
            draft_id=request.draft_id,
            track_name=request.track_name,
            params=request.params,
            width=request.width,
            height=request.height
        )
        
        result.success = True
        result.output = draft_result
        return JSONResponse(content=result.dict())

    except Exception as e:
        result.error = f"Error occurred while adding effect: {str(e)}."
        return JSONResponse(content=result.dict())

async def add_sticker(request: AddStickerRequest) -> JSONResponse:
    result = ResponseModel()

    # Validate required parameters
    if not request.sticker_id:
        result.error = "Hi, the required parameter 'sticker_id' is missing. Please add it and try again."
        return JSONResponse(content=result.dict())

    try:
        # Call add_sticker_impl method
        draft_result = add_sticker_impl(
            resource_id=request.sticker_id,
            start=request.start,
            end=request.end,
            draft_id=request.draft_id,
            transform_y=request.transform_y,
            transform_x=request.transform_x,
            alpha=request.alpha,
            flip_horizontal=request.flip_horizontal,
            flip_vertical=request.flip_vertical,
            rotation=request.rotation,
            scale_x=request.scale_x,
            scale_y=request.scale_y,
            track_name=request.track_name,
            relative_index=request.relative_index,
            width=request.width,
            height=request.height
        )

        result.success = True
        result.output = draft_result
        return JSONResponse(content=result.dict())

    except Exception as e:
        result.error = f"Error occurred while adding sticker: {str(e)}."
        return JSONResponse(content=result.dict()) 