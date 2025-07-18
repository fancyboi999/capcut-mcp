import pyJianYingDraft as draft
from settings.local import IS_CAPCUT_ENV
from util import generate_draft_url, hex_to_rgb
from pyJianYingDraft import trange, Font_type
from typing import Optional
from pyJianYingDraft import exceptions
from create_draft import get_or_create_draft
from pyJianYingDraft.text_segment import TextBubble, TextEffect

def add_text_impl(
    text: str,
    start: float,
    end: float,
    draft_id: str = None,
    transform_y: float = -0.8,
    transform_x: float = 0,
    font: str = "文轩体",  # Wenxuan Font
    font_color: str = "#ffffff",
    font_size: float = 8.0,
    track_name: str = "text_main",
    vertical: bool = False,  # Whether to display vertically
    font_alpha: float = 1.0,  # Transparency, range 0.0-1.0
    # Border parameters
    border_alpha: float = 1.0,
    border_color: str = "#000000",
    border_width: float = 0.0,  # Default no border display
    # Background parameters
    background_color: str = "#000000",
    background_style: int = 1,
    background_alpha: float = 0.0,  # Default no background display
    # Bubble effect
    bubble_effect_id: Optional[str] = None,
    bubble_resource_id: Optional[str] = None,
    # Text effect
    effect_effect_id: Optional[str] = None,
    intro_animation: Optional[str] = None,  # Intro animation type
    intro_duration: float = 0.5,  # Intro animation duration (seconds), default 0.5 seconds
    outro_animation: Optional[str] = None,  # Outro animation type
    outro_duration: float = 0.5,  # Outro animation duration (seconds), default 0.5 seconds
    width: int = 1080,
    height: int = 1920,
    fixed_width: float = -1,  # Text fixed width ratio, default -1 means not fixed
    fixed_height: float = -1,  # Text fixed height ratio, default -1 means not fixed
):
    """
    Add text subtitle to the specified draft (configurable parameter version)
    :param text: Text content
    :param start: Start time (seconds)
    :param end: End time (seconds)
    :param draft_id: Draft ID (optional, default None creates a new draft)
    :param transform_y: Y-axis position (default -0.8, bottom of screen)
    :param transform_x: X-axis position (default 0, center of screen)
    :param font: Font name (supports all fonts in Font_type)
    :param font_color: Font color #FFF0FF
    :param font_size: Font size (float value, default 8.0)
    :param track_name: Track name
    :param vertical: Whether to display vertically (default False)
    :param font_alpha: Text transparency, range 0.0-1.0 (default 1.0, completely opaque)
    :param border_alpha: Border transparency, range 0.0-1.0 (default 1.0)
    :param border_color: Border color (default black)
    :param border_width: Border width (default 0.0, no border display)
    :param background_color: Background color (default black)
    :param background_style: Background style (default 1)
    :param background_alpha: Background transparency (default 0.0, no background display)
    :param bubble_effect_id: Bubble effect ID
    :param bubble_resource_id: Bubble resource ID
    :param effect_effect_id: Text effect ID
    :param intro_animation: Intro animation type
    :param intro_duration: Intro animation duration (seconds), default 0.5 seconds
    :param outro_animation: Outro animation type
    :param outro_duration: Outro animation duration (seconds), default 0.5 seconds
    :param width: Video width (pixels)
    :param height: Video height (pixels)
    :param fixed_width: Text fixed width ratio, range 0.0-1.0, default -1 means not fixed
    :param fixed_height: Text fixed height ratio, range 0.0-1.0, default -1 means not fixed
    :return: Updated draft information
    """
    # Validate if font is in Font_type
    try:
        font_type = getattr(Font_type, font)
    except:
        available_fonts = [attr for attr in dir(Font_type) if not attr.startswith('_')]
        raise ValueError(f"Unsupported font: {font}, please use one of the fonts in Font_type: {available_fonts}")
    
    # Validate alpha value range
    if not 0.0 <= font_alpha <= 1.0:
        raise ValueError("alpha value must be between 0.0 and 1.0")
    if not 0.0 <= border_alpha <= 1.0:
        raise ValueError("border_alpha value must be between 0.0 and 1.0")
    if not 0.0 <= background_alpha <= 1.0:
        raise ValueError("background_alpha value must be between 0.0 and 1.0")
    
    # Get or create draft
    draft_id, script = get_or_create_draft(
        draft_id=draft_id,
        width=width,
        height=height
    )

    # Add text track
    if track_name is not None:
        try:
            imported_track = script.get_imported_track(draft.Track_type.text, name=track_name)
            # If no exception is thrown, the track already exists
        except exceptions.TrackNotFound:
            # Track doesn't exist, create a new track
            script.add_track(draft.Track_type.text, track_name=track_name)
    else:
        script.add_track(draft.Track_type.audio)

    # Convert hexadecimal color to RGB tuple
    try:
        rgb_color = hex_to_rgb(font_color)
        rgb_border_color = hex_to_rgb(border_color)
    except ValueError as e:
        raise ValueError(f"Color parameter error: {str(e)}")
    
    # Create text_border
    text_border = None
    if border_width > 0:
        text_border = draft.Text_border(
            alpha=border_alpha,
            color=rgb_border_color,
            width=border_width
        )
    
    # Create text_background
    text_background = None
    if background_alpha > 0:
        text_background = draft.Text_background(
            color=background_color,
            style=background_style,
            alpha=background_alpha
        )
    
    # Create bubble effect
    text_bubble = None
    if bubble_effect_id and bubble_resource_id:
        text_bubble = TextBubble(
            effect_id=bubble_effect_id,
            resource_id=bubble_resource_id
        )
    
    # Create text effect
    text_effect = None
    if effect_effect_id:
        text_effect = TextEffect(
            effect_id=effect_effect_id
        )
    
    # Convert ratio to pixel value
    pixel_fixed_width = -1
    pixel_fixed_height = -1
    if fixed_width > 0:
        pixel_fixed_width = int(fixed_width * script.width)
    if fixed_height > 0:
        pixel_fixed_height = int(fixed_height * script.height)
    
    # Create text segment (using configurable parameters)
    text_segment = draft.Text_segment(
        text,
        trange(f"{start}s", f"{end-start}s"),
        font=font_type,  # Use font from Font_type
        style=draft.Text_style(
            color=rgb_color,
            size=font_size,
            align=1,
            vertical=vertical,  # Set whether to display vertically
            alpha=font_alpha  # Set transparency
        ),
        clip_settings=draft.Clip_settings(transform_y=transform_y, transform_x=transform_x),
        border=text_border,
        background=text_background,
        fixed_width=pixel_fixed_width,
        fixed_height=pixel_fixed_height
    )

    if text_bubble:
        text_segment.add_bubble(text_bubble.effect_id, text_bubble.resource_id)
    if text_effect:
        text_segment.add_effect(text_effect.effect_id)

    # Add intro animation
    if intro_animation:
        try:
            if IS_CAPCUT_ENV:
                animation_type = getattr(draft.CapCut_Text_intro, intro_animation)
            else:
                animation_type = getattr(draft.Text_intro, intro_animation)
            # Convert seconds to microseconds
            duration_microseconds = int(intro_duration * 1000000)
            text_segment.add_animation(animation_type, duration_microseconds)  # Add intro animation, set duration
        except:
            print(f"Warning: Unsupported intro animation type {intro_animation}, this parameter will be ignored")

    # Add outro animation
    if outro_animation:
        try:
            if IS_CAPCUT_ENV:
                animation_type = getattr(draft.CapCut_Text_outro, outro_animation)
            else:
                animation_type = getattr(draft.Text_outro, outro_animation)
            # Convert seconds to microseconds
            duration_microseconds = int(outro_duration * 1000000)
            text_segment.add_animation(animation_type, duration_microseconds)  # Add outro animation, set duration
        except:
            print(f"Warning: Unsupported outro animation type {outro_animation}, this parameter will be ignored")

    # Add text segment to track
    script.add_segment(text_segment, track_name=track_name)

    return {
        "draft_id": draft_id,
        "draft_url": generate_draft_url(draft_id)
    }
