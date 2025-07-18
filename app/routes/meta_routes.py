from fastapi import APIRouter
from app.controllers import (
    get_intro_animation_types,
    get_outro_animation_types,
    get_combo_animation_types,
    get_transition_types,
    get_mask_types,
    get_audio_effect_types,
    get_font_types,
    get_text_intro_types,
    get_text_outro_types,
    get_text_loop_anim_types,
    get_video_scene_effect_types,
    get_video_character_effect_types
)

router = APIRouter(tags=["元数据"])

@router.get('/get_intro_animation_types',operation_id='get_intro_animation_types')
async def get_intro_animation_types_route():
    return await get_intro_animation_types()

@router.get('/get_outro_animation_types',operation_id='get_outro_animation_types')
async def get_outro_animation_types_route():
    return await get_outro_animation_types()

@router.get('/get_combo_animation_types',operation_id='get_combo_animation_types')
async def get_combo_animation_types_route():
    return await get_combo_animation_types()

@router.get('/get_transition_types',operation_id='get_transition_types')
async def get_transition_types_route():
    return await get_transition_types()

@router.get('/get_mask_types',operation_id='get_mask_types')
async def get_mask_types_route():
    return await get_mask_types()

@router.get('/get_audio_effect_types',operation_id='get_audio_effect_types')
async def get_audio_effect_types_route():
    return await get_audio_effect_types()

@router.get('/get_font_types',operation_id='get_font_types')
async def get_font_types_route():
    return await get_font_types()

@router.get('/get_text_intro_types',operation_id='get_text_intro_types')
async def get_text_intro_types_route():
    return await get_text_intro_types()

@router.get('/get_text_outro_types',operation_id='get_text_outro_types')
async def get_text_outro_types_route():
    return await get_text_outro_types()

@router.get('/get_text_loop_anim_types',operation_id='get_text_loop_anim_types')
async def get_text_loop_anim_types_route():
    return await get_text_loop_anim_types()

@router.get('/get_video_scene_effect_types',operation_id='get_video_scene_effect_types')
async def get_video_scene_effect_types_route():
    return await get_video_scene_effect_types()

@router.get('/get_video_character_effect_types',operation_id='get_video_character_effect_types')
async def get_video_character_effect_types_route():
    return await get_video_character_effect_types() 