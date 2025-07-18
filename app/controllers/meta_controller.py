from fastapi.responses import JSONResponse
from app.schemas import ResponseModel
import pyJianYingDraft as draft
from pyJianYingDraft.metadata.animation_meta import Intro_type, Outro_type, Group_animation_type
from pyJianYingDraft.metadata.capcut_animation_meta import CapCut_Intro_type, CapCut_Outro_type, CapCut_Group_animation_type
from pyJianYingDraft.metadata.transition_meta import Transition_type
from pyJianYingDraft.metadata.capcut_transition_meta import CapCut_Transition_type
from pyJianYingDraft.metadata.mask_meta import Mask_type
from pyJianYingDraft.metadata.capcut_mask_meta import CapCut_Mask_type
from pyJianYingDraft.metadata.audio_effect_meta import Tone_effect_type, Audio_scene_effect_type, Speech_to_song_type
from pyJianYingDraft.metadata.capcut_audio_effect_meta import CapCut_Voice_filters_effect_type, CapCut_Voice_characters_effect_type, CapCut_Speech_to_song_effect_type
from pyJianYingDraft.metadata.font_meta import Font_type
from pyJianYingDraft.metadata.animation_meta import Text_intro, Text_outro, Text_loop_anim
from pyJianYingDraft.metadata.capcut_text_animation_meta import CapCut_Text_intro, CapCut_Text_outro, CapCut_Text_loop_anim
from pyJianYingDraft.metadata.video_effect_meta import Video_scene_effect_type, Video_character_effect_type
from pyJianYingDraft.metadata.capcut_effect_meta import CapCut_Video_scene_effect_type, CapCut_Video_character_effect_type
from settings.local import IS_CAPCUT_ENV

async def get_intro_animation_types() -> JSONResponse:
    """Return supported entrance animation type list
    
    If IS_CAPCUT_ENV is True, return entrance animation types in CapCut environment
    Otherwise return entrance animation types in JianYing environment
    """
    result = ResponseModel(success=True)
    
    try:
        animation_types = []
        
        if IS_CAPCUT_ENV:
            # Return entrance animation types in CapCut environment
            for name, member in CapCut_Intro_type.__members__.items():
                animation_types.append({
                    "name": name
                })
        else:
            # Return entrance animation types in JianYing environment
            for name, member in Intro_type.__members__.items():
                animation_types.append({
                    "name": name
                })
        
        result.output = animation_types
        return JSONResponse(content=result.dict())
    
    except Exception as e:
        result.success = False
        result.error = f"Error occurred while getting entrance animation types: {str(e)}"
        return JSONResponse(content=result.dict())

async def get_outro_animation_types() -> JSONResponse:
    """Return supported exit animation type list
    
    If IS_CAPCUT_ENV is True, return exit animation types in CapCut environment
    Otherwise return exit animation types in JianYing environment
    """
    result = ResponseModel(success=True)
    
    try:
        animation_types = []
        
        if IS_CAPCUT_ENV:
            # Return exit animation types in CapCut environment
            for name, member in CapCut_Outro_type.__members__.items():
                animation_types.append({
                    "name": name
                })
        else:
            # Return exit animation types in JianYing environment
            for name, member in Outro_type.__members__.items():
                animation_types.append({
                    "name": name
                })
        
        result.output = animation_types
        return JSONResponse(content=result.dict())
    
    except Exception as e:
        result.success = False
        result.error = f"Error occurred while getting exit animation types: {str(e)}"
        return JSONResponse(content=result.dict())

async def get_combo_animation_types() -> JSONResponse:
    """Return supported combo animation type list
    
    If IS_CAPCUT_ENV is True, return combo animation types in CapCut environment
    Otherwise return combo animation types in JianYing environment
    """
    result = ResponseModel(success=True)
    
    try:
        animation_types = []
        
        if IS_CAPCUT_ENV:
            # Return combo animation types in CapCut environment
            for name, member in CapCut_Group_animation_type.__members__.items():
                animation_types.append({
                    "name": name
                })
        else:
            # Return combo animation types in JianYing environment
            for name, member in Group_animation_type.__members__.items():
                animation_types.append({
                    "name": name
                })
        
        result.output = animation_types
        return JSONResponse(content=result.dict())
    
    except Exception as e:
        result.success = False
        result.error = f"Error occurred while getting combo animation types: {str(e)}"
        return JSONResponse(content=result.dict())

async def get_transition_types() -> JSONResponse:
    """Return supported transition animation type list
    
    If IS_CAPCUT_ENV is True, return transition animation types in CapCut environment
    Otherwise return transition animation types in JianYing environment
    """
    result = ResponseModel(success=True)
    
    try:
        transition_types = []
        
        if IS_CAPCUT_ENV:
            # Return transition animation types in CapCut environment
            for name, member in CapCut_Transition_type.__members__.items():
                transition_types.append({
                    "name": name
                })
        else:
            # Return transition animation types in JianYing environment
            for name, member in Transition_type.__members__.items():
                transition_types.append({
                    "name": name
                })
        
        result.output = transition_types
        return JSONResponse(content=result.dict())
    
    except Exception as e:
        result.success = False
        result.error = f"Error occurred while getting transition animation types: {str(e)}"
        return JSONResponse(content=result.dict())

async def get_mask_types() -> JSONResponse:
    """Return supported mask type list
    
    If IS_CAPCUT_ENV is True, return mask types in CapCut environment
    Otherwise return mask types in JianYing environment
    """
    result = ResponseModel(success=True)
    
    try:
        mask_types = []
        
        if IS_CAPCUT_ENV:
            # Return mask types in CapCut environment
            for name, member in CapCut_Mask_type.__members__.items():
                mask_types.append({
                    "name": name
                })
        else:
            # Return mask types in JianYing environment
            for name, member in Mask_type.__members__.items():
                mask_types.append({
                    "name": name
                })
        
        result.output = mask_types
        return JSONResponse(content=result.dict())
    
    except Exception as e:
        result.success = False
        result.error = f"Error occurred while getting mask types: {str(e)}"
        return JSONResponse(content=result.dict())

async def get_audio_effect_types() -> JSONResponse:
    """Return supported audio effect type list
    
    If IS_CAPCUT_ENV is True, return audio effect types in CapCut environment
    Otherwise return audio effect types in JianYing environment
    
    The returned structure includes name, type and Effect_param information
    """
    result = ResponseModel(success=True)
    
    try:
        audio_effect_types = []
        
        if IS_CAPCUT_ENV:
            # Return audio effect types in CapCut environment
            # 1. Voice filters effect types
            for name, member in CapCut_Voice_filters_effect_type.__members__.items():
                params_info = []
                for param in member.value.params:
                    params_info.append({
                        "name": param.name,
                        "default_value": param.default_value * 100,
                        "min_value": param.min_value * 100,
                        "max_value": param.max_value * 100
                    })
                
                audio_effect_types.append({
                    "name": name,
                    "type": "Voice_filters",
                    "params": params_info
                })
            
            # 2. Voice characters effect types
            for name, member in CapCut_Voice_characters_effect_type.__members__.items():
                params_info = []
                for param in member.value.params:
                    params_info.append({
                        "name": param.name,
                        "default_value": param.default_value * 100,
                        "min_value": param.min_value * 100,
                        "max_value": param.max_value * 100
                    })
                
                audio_effect_types.append({
                    "name": name,
                    "type": "Voice_characters",
                    "params": params_info
                })
            
            # 3. Speech to song effect types
            for name, member in CapCut_Speech_to_song_effect_type.__members__.items():
                params_info = []
                for param in member.value.params:
                    params_info.append({
                        "name": param.name,
                        "default_value": param.default_value * 100,
                        "min_value": param.min_value * 100,
                        "max_value": param.max_value * 100
                    })
                
                audio_effect_types.append({
                    "name": name,
                    "type": "Speech_to_song",
                    "params": params_info
                })
        else:
            # Return audio effect types in JianYing environment
            # 1. Tone effect types
            for name, member in Tone_effect_type.__members__.items():
                params_info = []
                for param in member.value.params:
                    params_info.append({
                        "name": param.name,
                        "default_value": param.default_value * 100,
                        "min_value": param.min_value * 100,
                        "max_value": param.max_value * 100
                    })
                
                audio_effect_types.append({
                    "name": name,
                    "type": "Tone",
                    "params": params_info
                })
            
            # 2. Audio scene effect types
            for name, member in Audio_scene_effect_type.__members__.items():
                params_info = []
                for param in member.value.params:
                    params_info.append({
                        "name": param.name,
                        "default_value": param.default_value * 100,
                        "min_value": param.min_value * 100,
                        "max_value": param.max_value * 100
                    })
                
                audio_effect_types.append({
                    "name": name,
                    "type": "Audio_scene",
                    "params": params_info
                })
            
            # 3. Speech to song effect types
            for name, member in Speech_to_song_type.__members__.items():
                params_info = []
                for param in member.value.params:
                    params_info.append({
                        "name": param.name,
                        "default_value": param.default_value * 100,
                        "min_value": param.min_value * 100,
                        "max_value": param.max_value * 100
                    })
                
                audio_effect_types.append({
                    "name": name,
                    "type": "Speech_to_song",
                    "params": params_info
                })
        
        result.output = audio_effect_types
        return JSONResponse(content=result.dict())
    
    except Exception as e:
        result.success = False
        result.error = f"Error occurred while getting audio effect types: {str(e)}"
        return JSONResponse(content=result.dict())

async def get_font_types() -> JSONResponse:
    """Return supported font type list
    
    Return font types in JianYing environment
    """
    result = ResponseModel(success=True)
    
    try:
        font_types = []
        
        # Return font types in JianYing environment
        for name, member in Font_type.__members__.items():
            font_types.append({
                "name": name
            })
        
        result.output = font_types
        return JSONResponse(content=result.dict())
    
    except Exception as e:
        result.success = False
        result.error = f"Error occurred while getting font types: {str(e)}"
        return JSONResponse(content=result.dict())

async def get_text_intro_types() -> JSONResponse:
    """Return supported text entrance animation type list
    
    If IS_CAPCUT_ENV is True, return text entrance animation types in CapCut environment
    Otherwise return text entrance animation types in JianYing environment
    """
    result = ResponseModel(success=True)
    
    try:
        text_intro_types = []
        
        if IS_CAPCUT_ENV:
            # Return text entrance animation types in CapCut environment
            for name, member in CapCut_Text_intro.__members__.items():
                text_intro_types.append({
                    "name": name
                })
        else:
            # Return text entrance animation types in JianYing environment
            for name, member in Text_intro.__members__.items():
                text_intro_types.append({
                    "name": name
                })
        
        result.output = text_intro_types
        return JSONResponse(content=result.dict())
    
    except Exception as e:
        result.success = False
        result.error = f"Error occurred while getting text entrance animation types: {str(e)}"
        return JSONResponse(content=result.dict())

async def get_text_outro_types() -> JSONResponse:
    """Return supported text exit animation type list
    
    If IS_CAPCUT_ENV is True, return text exit animation types in CapCut environment
    Otherwise return text exit animation types in JianYing environment
    """
    result = ResponseModel(success=True)
    
    try:
        text_outro_types = []
        
        if IS_CAPCUT_ENV:
            # Return text exit animation types in CapCut environment
            for name, member in CapCut_Text_outro.__members__.items():
                text_outro_types.append({
                    "name": name
                })
        else:
            # Return text exit animation types in JianYing environment
            for name, member in Text_outro.__members__.items():
                text_outro_types.append({
                    "name": name
                })
        
        result.output = text_outro_types
        return JSONResponse(content=result.dict())
    
    except Exception as e:
        result.success = False
        result.error = f"Error occurred while getting text exit animation types: {str(e)}"
        return JSONResponse(content=result.dict())

async def get_text_loop_anim_types() -> JSONResponse:
    """Return supported text loop animation type list
    
    If IS_CAPCUT_ENV is True, return text loop animation types in CapCut environment
    Otherwise return text loop animation types in JianYing environment
    """
    result = ResponseModel(success=True)
    
    try:
        text_loop_anim_types = []
        
        if IS_CAPCUT_ENV:
            # Return text loop animation types in CapCut environment
            for name, member in CapCut_Text_loop_anim.__members__.items():
                text_loop_anim_types.append({
                    "name": name
                })
        else:
            # Return text loop animation types in JianYing environment
            for name, member in Text_loop_anim.__members__.items():
                text_loop_anim_types.append({
                    "name": name
                })
        
        result.output = text_loop_anim_types
        return JSONResponse(content=result.dict())
    
    except Exception as e:
        result.success = False
        result.error = f"Error occurred while getting text loop animation types: {str(e)}"
        return JSONResponse(content=result.dict())

async def get_video_scene_effect_types() -> JSONResponse:
    """Return supported scene effect type list
    
    If IS_CAPCUT_ENV is True, return scene effect types in CapCut environment
    Otherwise return scene effect types in JianYing environment
    """
    result = ResponseModel(success=True)
    
    try:
        effect_types = []
        
        if IS_CAPCUT_ENV:
            # Return scene effect types in CapCut environment
            for name, member in CapCut_Video_scene_effect_type.__members__.items():
                effect_types.append({
                    "name": name
                })
        else:
            # Return scene effect types in JianYing environment
            for name, member in Video_scene_effect_type.__members__.items():
                effect_types.append({
                    "name": name
                })
        
        result.output = effect_types
        return JSONResponse(content=result.dict())
    
    except Exception as e:
        result.success = False
        result.error = f"Error occurred while getting scene effect types: {str(e)}"
        return JSONResponse(content=result.dict())

async def get_video_character_effect_types() -> JSONResponse:
    """Return supported character effect type list
    
    If IS_CAPCUT_ENV is True, return character effect types in CapCut environment
    Otherwise return character effect types in JianYing environment
    """
    result = ResponseModel(success=True)
    
    try:
        effect_types = []
        
        if IS_CAPCUT_ENV:
            # Return character effect types in CapCut environment
            for name, member in CapCut_Video_character_effect_type.__members__.items():
                effect_types.append({
                    "name": name
                })
        else:
            # Return character effect types in JianYing environment
            for name, member in Video_character_effect_type.__members__.items():
                effect_types.append({
                    "name": name
                })
        
        result.output = effect_types
        return JSONResponse(content=result.dict())
    
    except Exception as e:
        result.success = False
        result.error = f"Error occurred while getting character effect types: {str(e)}"
        return JSONResponse(content=result.dict()) 