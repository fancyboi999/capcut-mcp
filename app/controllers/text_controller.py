from fastapi.responses import JSONResponse
from app.schemas import AddTextRequest, AddSubtitleRequest, ResponseModel
from add_text_impl import add_text_impl
from add_subtitle_impl import add_subtitle_impl

async def add_text(request: AddTextRequest) -> JSONResponse:
    result = ResponseModel()

    # Validate required parameters
    if not request.text or request.start is None or request.end is None:
        result.error = "Hi, the required parameters 'text', 'start' or 'end' are missing."
        return JSONResponse(content=result.dict())

    try:
        # Call add_text_impl method
        draft_result = add_text_impl(
            text=request.text,
            start=request.start,
            end=request.end,
            draft_id=request.draft_id,
            transform_y=request.transform_y,
            transform_x=request.transform_x,
            font=request.font,
            font_color=request.font_color,
            font_size=request.font_size,
            track_name=request.track_name,
            vertical=request.vertical,
            font_alpha=request.font_alpha,
            border_alpha=request.border_alpha,
            border_color=request.border_color,
            border_width=request.border_width,
            background_color=request.background_color,
            background_style=request.background_style,
            background_alpha=request.background_alpha,
            bubble_effect_id=request.bubble_effect_id,
            bubble_resource_id=request.bubble_resource_id,
            effect_effect_id=request.effect_effect_id,
            intro_animation=request.intro_animation,
            intro_duration=request.intro_duration,
            outro_animation=request.outro_animation,
            outro_duration=request.outro_duration,
            width=request.width,
            height=request.height,
            fixed_width=request.fixed_width,
            fixed_height=request.fixed_height
        )
        
        result.success = True
        result.output = draft_result
        return JSONResponse(content=result.dict())

    except Exception as e:
        result.error = f"Error occurred while processing text: {str(e)}."
        return JSONResponse(content=result.dict())

async def add_subtitle(request: AddSubtitleRequest) -> JSONResponse:
    result = ResponseModel()

    # Validate required parameters
    if not request.srt:
        result.error = "Hi, the required parameters 'srt' are missing."
        return JSONResponse(content=result.dict())

    try:
        # Call add_subtitle_impl method
        draft_result = add_subtitle_impl(
            srt_path=request.srt,
            draft_id=request.draft_id,
            track_name=request.track_name,
            time_offset=request.time_offset,
            # Font style parameters
            font_size=request.font_size,
            bold=request.bold,
            italic=request.italic,
            underline=request.underline,
            font_color=request.font_color,
            vertical=request.vertical,
            alpha=request.alpha,
            border_alpha=request.border_alpha,
            border_color=request.border_color,
            border_width=request.border_width,
            background_color=request.background_color,
            background_style=request.background_style,
            background_alpha=request.background_alpha,
            # Image adjustment parameters
            transform_x=request.transform_x,
            transform_y=request.transform_y,
            scale_x=request.scale_x,
            scale_y=request.scale_y,
            rotation=request.rotation,
            width=request.width,
            height=request.height
        )
        
        result.success = True
        result.output = draft_result
        return JSONResponse(content=result.dict())

    except Exception as e:
        result.error = f"Error occurred while processing subtitle: {str(e)}."
        return JSONResponse(content=result.dict()) 