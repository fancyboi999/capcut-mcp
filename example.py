import requests
import json
import sys
import time
from util import timing_decorator
import functools
import threading


# Base URL of the service, please modify according to actual situation
BASE_URL = "http://localhost:9000"
LICENSE_KEY = "539C3FEB-74AE48D4-A964D52B-C520F801"  # Using trial version license key

def make_request(endpoint, data, method='POST'):
    """Send HTTP request to the server and handle the response"""
    url = f"{BASE_URL}/{endpoint}"
    headers = {'Content-Type': 'application/json'}
    
    try:
        if method == 'POST':
            response = requests.post(url, data=json.dumps(data), headers=headers)
        elif method == 'GET':
            response = requests.get(url, params=data, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
            
        response.raise_for_status()  # Raise an exception if the request fails
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Unable to parse server response")
        sys.exit(1)

def add_audio_track(audio_url, start, end, target_start, volume=1.0, 
                    speed=1.0, track_name="main_audio", effect_type=None, effect_params=None, draft_id=None):
    """API call to add audio track"""
    data = {
        "license_key": LICENSE_KEY,  # Using trial version license key
        "audio_url": audio_url,
        "start": start,
        "end": end,
        "target_start": target_start,
        "volume": volume,
        "speed": speed,
        "track_name": track_name,
        "effect_type": effect_type,
        "effect_params": effect_params
    }
    
    if draft_id:
        data["draft_id"] = draft_id
        
    return make_request("add_audio", data)

def add_text_impl(text, start, end, font, font_color, font_size, track_name,draft_folder="123", draft_id=None,
                  vertical=False, transform_x=0.5, transform_y=0.5, font_alpha=1.0,
                  border_color=None, border_width=0.0, border_alpha=1.0,
                  background_color=None, background_alpha=1.0, background_style=None,
                  bubble_effect_id=None, bubble_resource_id=None,
                  effect_effect_id=None, outro_animation=None):
    """API call to add text"""
    data = {
        "license_key": LICENSE_KEY,  # Using trial version license key
        "draft_folder": draft_folder,
        "text": text,
        "start": start,
        "end": end,
        "font": font,
        "color": font_color,
        "size": font_size,
        "alpha": font_alpha,
        "track_name": track_name,
        "vertical": vertical,
        "transform_x": transform_x,
        "transform_y": transform_y
    }
    
    # Add border parameters
    if border_color:
        data["border_color"] = border_color
        data["border_width"] = border_width
        data["border_alpha"] = border_alpha
    
    # Add background parameters
    if background_color:
        data["background_color"] = background_color
        data["background_alpha"] = background_alpha
        if background_style:
            data["background_style"] = background_style
    
    # Add bubble effect parameters
    if bubble_effect_id:
        data["bubble_effect_id"] = bubble_effect_id
        if bubble_resource_id:
            data["bubble_resource_id"] = bubble_resource_id
    
    # Add text effect parameters
    if effect_effect_id:
        data["effect_effect_id"] = effect_effect_id
    
    if draft_id:
        data["draft_id"] = draft_id
        
    if outro_animation:
        data["outro_animation"] = outro_animation
        
    return make_request("add_text", data)

def add_image_impl(image_url, width, height, start, end, track_name, draft_id=None,
                  transform_x=0, transform_y=0, scale_x=1.0, scale_y=1.0, transition=None, transition_duration=None,
                  # New mask-related parameters
                  mask_type=None, mask_center_x=0.0, mask_center_y=0.0, mask_size=0.5,
                  mask_rotation=0.0, mask_feather=0.0, mask_invert=False,
                  mask_rect_width=None, mask_round_corner=None):
    """API call to add image"""
    data = {
        "license_key": LICENSE_KEY,  # Using trial version license key
        "image_url": image_url,
        "width": width,
        "height": height,
        "start": start,
        "end": end,
        "track_name": track_name,
        "transform_x": transform_x,
        "transform_y": transform_y,
        "scale_x": scale_x,
        "scale_y": scale_y,
        "transition": transition,
        "transition_duration": transition_duration or 0.5,  # Default transition duration is 0.5 seconds
        # Add mask-related parameters
        "mask_type": mask_type,
        "mask_center_x": mask_center_x,
        "mask_center_y": mask_center_y,
        "mask_size": mask_size,
        "mask_rotation": mask_rotation,
        "mask_feather": mask_feather,
        "mask_invert": mask_invert,
        "mask_rect_width": mask_rect_width,
        "mask_round_corner": mask_round_corner
    }
    
    if draft_id:
        data["draft_id"] = draft_id
        
    return make_request("add_image", data)

def generate_image_impl(prompt, width, height, start, end, track_name, draft_id=None,
                  transform_x=0, transform_y=0, scale_x=1.0, scale_y=1.0, transition=None, transition_duration=None):
    """API call to add image"""
    data = {
        "license_key": LICENSE_KEY,  # Using trial version license key
        "prompt": prompt,
        "width": width,
        "height": height,
        "start": start,
        "end": end,
        "track_name": track_name,
        "transform_x": transform_x,
        "transform_y": transform_y,
        "scale_x": scale_x,
        "scale_y": scale_y,
        "transition": transition,
        "transition_duration": transition_duration or 0.5  # Default transition duration is 0.5 seconds
    }
    
    if draft_id:
        data["draft_id"] = draft_id
        
    return make_request("generate_image", data)

def add_sticker_impl(resource_id, start, end, draft_id=None, transform_x=0, transform_y=0,
                    alpha=1.0, flip_horizontal=False, flip_vertical=False, rotation=0.0,
                    scale_x=1.0, scale_y=1.0, track_name="sticker_main", relative_index=0,
                    width=1080, height=1920):
    """API call to add sticker"""
    data = {
        "license_key": LICENSE_KEY,  # Using trial version license key
        "sticker_id": resource_id,
        "start": start,
        "end": end,
        "transform_x": transform_x,
        "transform_y": transform_y,
        "alpha": alpha,
        "flip_horizontal": flip_horizontal,
        "flip_vertical": flip_vertical,
        "rotation": rotation,
        "scale_x": scale_x,
        "scale_y": scale_y,
        "track_name": track_name,
        "relative_index": relative_index,
        "width": width,
        "height": height
    }
    
    if draft_id:
        data["draft_id"] = draft_id
        
    return make_request("add_sticker", data)

def add_video_keyframe_impl(draft_id, track_name, property_type=None, time=None, value=None, 
                           property_types=None, times=None, values=None):
    """API call to add video keyframe
    
    Supports two modes:
    1. Single keyframe: using property_type, time, value parameters
    2. Batch keyframes: using property_types, times, values parameters (in list form)
    """
    data = {
        "license_key": LICENSE_KEY,  # Using trial version license key
        "draft_id": draft_id,
        "track_name": track_name
    }
    
    # Add single keyframe parameters (if provided)
    if property_type is not None:
        data["property_type"] = property_type
    if time is not None:
        data["time"] = time
    if value is not None:
        data["value"] = value
    
    # Add batch keyframe parameters (if provided)
    if property_types is not None:
        data["property_types"] = property_types
    if times is not None:
        data["times"] = times
    if values is not None:
        data["values"] = values
    
    return make_request("add_video_keyframe", data)

def add_video_impl(video_url, start=None, end=None, width=None, height=None, track_name="main",
                   draft_id=None, transform_y=0, scale_x=1, scale_y=1, transform_x=0,
                   speed=1.0, target_start=0, relative_index=0, transition=None, transition_duration=None,
                   # Mask-related parameters
                   mask_type=None, mask_center_x=0.5, mask_center_y=0.5, mask_size=1.0,
                   mask_rotation=0.0, mask_feather=0.0, mask_invert=False,
                   mask_rect_width=None, mask_round_corner=None):
    """API call to add video track"""
    data = {
        "license_key": LICENSE_KEY,  # Using trial version license key
        "video_url": video_url,
        "height": height,
        "track_name": track_name,
        "transform_y": transform_y,
        "scale_x": scale_x,
        "scale_y": scale_y,
        "transform_x": transform_x,
        "speed": speed,
        "target_start": target_start,
        "relative_index": relative_index,
        "transition": transition,
        "transition_duration": transition_duration or 0.5,  # Default transition duration is 0.5 seconds
        # Mask-related parameters
        "mask_type": mask_type,
        "mask_center_x": mask_center_x,
        "mask_center_y": mask_center_y,
        "mask_size": mask_size,
        "mask_rotation": mask_rotation,
        "mask_feather": mask_feather,
        "mask_invert": mask_invert,
        "mask_rect_width": mask_rect_width,
        "mask_round_corner": mask_round_corner
    }
    if start:
        data["start"] = start
    if end:
        data["end"] = end
    if width:
        data["width"] = width
    if height:
        data["height"] = height
    return make_request("add_video", data)

def add_effect(effect_type, start, end, draft_id=None, track_name="effect_01",
              params=None, width=1080, height=1920):
    """API call to add effect"""
    data = {
        "license_key": LICENSE_KEY,  # Using trial version license key
        "effect_type": effect_type,
        "start": start,
        "end": end,
        "track_name": track_name,
        "params": params or [],
        "width": width,
        "height": height
    }
    
    if draft_id:
        data["draft_id"] = draft_id
        
    return make_request("add_effect", data)

def test_effect_01():
    """Test adding effect service"""
    # draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    draft_folder = "/Users/sunguannan/Movies/CapCut/User Data/Projects/com.lveditor.draft"
    
    print("\nTest: Adding effect")
    effect_result = add_effect(
        start=0,
        end=5,
        track_name="effect_01",
        # effect_type="金粉闪闪",  # Example using glow effect
        effect_type="Gold_Sparkles",
        params=[100, 50, 34]  # Example parameters, depending on the specific effect type
    )
    print(f"Effect adding result: {effect_result}")
    print(save_draft_impl(effect_result['output']['draft_id'], draft_folder))
    
    # If needed, you can add other test cases here
    
    # Return the first test result for subsequent operations (if any)
    return effect_result


def test_text():
    """Test adding text"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"

    # Test case 1: Basic text addition
    print("\nTest: Adding basic text")
    text_result = add_text_impl(
        text="Hello, I am CapCut Assistant",
        start=0,
        end=3,
        font="思源中宋",
        font_color="#FF0000",  # Red
        track_name="main_text",
        transform_y=0.8,
        transform_x=0.5,
        font_size=30.0
    )
    print("Test case 1 (Basic text) successful:", text_result)

    # Test case 2: Vertical text
    result2 = add_text_impl(
        draft_id=text_result['output']['draft_id'],
        text="Vertical text demo",
        start=3,
        end=6,
        font="云书法三行魏碑体",
        font_color="#00FF00",  # Green
        font_size=8.0,
        track_name="main_text",
        vertical=True,  # Enable vertical text
        transform_y=-0.5,
        outro_animation='Blur'
    )
    print("Test case 2 (Vertical text) successful:", result2)

    # Test case 3: Text with border and background
    result3 = add_text_impl(
        draft_id=result2['output']['draft_id'],
        text="Border and background test",
        start=6,
        end=9,
        font="思源中宋",
        font_color="#FFFFFF",  # White text
        font_size=24.0,
        track_name="main_text",
        transform_y=0.0,
        transform_x=0.5,
        border_color="#FF0000",  # Black border
        border_width=20.0,
        border_alpha=1.0,
        background_color="#0000FF",  # Blue background
        background_alpha=0.5,  # Semi-transparent background
        background_style=0  # Bubble style background
    )
    print("Test case 3 (Border and background) successful:", result3)
    
    # Finally save and upload the draft
    if result3.get('success') and result3.get('output'):
        save_result = save_draft_impl(result3['output']['draft_id'],draft_folder)
        print(f"Draft save result: {save_result}")
    
    # Return the last test result for subsequent operations (if any)
    return result3


def test_image01():
    """Test adding image"""
    # draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    draft_folder = "/Users/sunguannan/Movies/CapCut/User Data/Projects/com.lveditor.draft"

    print("\nTest: Adding image 1")
    image_result = add_image_impl(
        image_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_image_v2/d6e33c84d7554146a25b1093b012838b_0.png?x-oss-process=image/resize,w_500/watermark,image_aW1nL3dhdGVyMjAyNDExMjkwLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSxtX2ZpeGVkLHdfMTQ1LGhfMjU=,t_80,g_se,x_10,y_10/format,webp",
        width=480,
        height=480,
        start=0,
        end=5.0,
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main"
    )
    print(f"Image added successfully! {image_result['output']['draft_id']}")
    print(save_draft_impl(image_result['output']['draft_id'], draft_folder))


def test_image02():
    """Test adding multiple images"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"

    print("\nTest: Adding image 1")
    image_result = add_image_impl(
        image_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_image_v2/d6e33c84d7554146a25b1093b012838b_0.png?x-oss-process=image/resize,w_500/watermark,image_aW1nL3dhdGVyMjAyNDExMjkwLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSxtX2ZpeGVkLHdfMTQ1LGhfMjU=,t_80,g_se,x_10,y_10/format,webp",
        width=480,
        height=480,
        start=0,
        end=5.0,
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main"
    )
    print(f"Image 1 added successfully! {image_result['output']['draft_id']}")
    
    print("\nTest: Adding image 2")
    image_result = add_image_impl(
        draft_id=image_result['output']['draft_id'],
        image_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_image_v2/d6e33c84d7554146a25b1093b012838b_0.png?x-oss-process=image/resize,w_500/watermark,image_aW1nL3dhdGVyMjAyNDExMjkwLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSxtX2ZpeGVkLHdfMTQ1LGhfMjU=,t_80,g_se,x_10,y_10/format,webp",
        width=480,
        height=480,
        start=5,
        end=10.0,
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main"
    )
    print(f"Image 2 added successfully! {image_result['output']['draft_id']}")
    print(save_draft_impl(image_result['output']['draft_id'], draft_folder))


def test_image03():
    """Test adding images to different tracks"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"

    print("\nTest: Adding image 1")
    image_result = add_image_impl(
        image_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_image_v2/d6e33c84d7554146a25b1093b012838b_0.png?x-oss-process=image/resize,w_500/watermark,image_aW1nL3dhdGVyMjAyNDExMjkwLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSxtX2ZpeGVkLHdfMTQ1LGhfMjU=,t_80,g_se,x_10,y_10/format,webp",
        width=480,
        height=480,
        start=0,
        end=5.0,
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main"
    )
    print(f"Image 1 added successfully! {image_result['output']['draft_id']}")
    
    print("\nTest: Adding image 2")
    image_result = add_image_impl(
        draft_id=image_result['output']['draft_id'],
        image_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_image_v2/d6e33c84d7554146a25b1093b012838b_0.png?x-oss-process=image/resize,w_500/watermark,image_aW1nL3dhdGVyMjAyNDExMjkwLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSxtX2ZpeGVkLHdfMTQ1LGhfMjU=,t_80,g_se,x_10,y_10/format,webp",
        width=480,
        height=480,
        start=5,
        end=10.0,
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main"
    )
    print(f"Image 2 added successfully! {image_result['output']['draft_id']}")

    print("\nTest: Adding image 3")
    image_result = add_image_impl(
        draft_id=image_result['output']['draft_id'],
        image_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_image_v2/d6e33c84d7554146a25b1093b012838b_0.png?x-oss-process=image/resize,w_500/watermark,image_aW1nL3dhdGVyMjAyNDExMjkwLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSxtX2ZpeGVkLHdfMTQ1LGhfMjU=,t_80,g_se,x_10,y_10/format,webp",
        width=480,
        height=480,
        start=10,
        end=15.0,
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main_2"  # Use different track name
    )
    print(f"Image 3 added successfully! {image_result['output']['draft_id']}")
    query_draft_status_impl_polling(image_result['output']['draft_id'])
    save_draft_impl(image_result['output']['draft_id'], draft_folder)

def test_image04():
    """Test adding image"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"

    print("\nTest: Adding image 1")
    image_result = add_image_impl(
        image_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_image_v2/d6e33c84d7554146a25b1093b012838b_0.png?x-oss-process=image/resize,w_500/watermark,image_aW1nL3dhdGVyMjAyNDExMjkwLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSxtX2ZpeGVkLHdfMTQ1LGhfMjU=,t_80,g_se,x_10,y_10/format,webp",
        width=480,
        height=480,
        start=5.0,
        end=10.0,
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="image_main"
    )
    print(f"Image added successfully! {image_result['output']['draft_id']}")
    print(save_draft_impl(image_result['output']['draft_id'], draft_folder))


def test_mask_01():
    """Test adding images to different tracks"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"

    print("\nTest: Adding image 1")
    image_result = add_image_impl(
        image_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_image_v2/d6e33c84d7554146a25b1093b012838b_0.png?x-oss-process=image/resize,w_500/watermark,image_aW1nL3dhdGVyMjAyNDExMjkwLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSxtX2ZpeGVkLHdfMTQ1LGhfMjU=,t_80,g_se,x_10,y_10/format,webp",
        width=480,
        height=480,
        start=0,
        end=5.0,
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main"
    )
    print(f"Image 1 added successfully! {image_result['output']['draft_id']}")
    
    print("\nTest: Adding image 2")
    image_result = add_image_impl(
        draft_id=image_result['output']['draft_id'],
        image_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_image_v2/d6e33c84d7554146a25b1093b012838b_0.png?x-oss-process=image/resize,w_500/watermark,image_aW1nL3dhdGVyMjAyNDExMjkwLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSxtX2ZpeGVkLHdfMTQ1LGhfMjU=,t_80,g_se,x_10,y_10/format,webp",
        width=480,
        height=480,
        start=5,
        end=10.0,
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main"
    )
    print(f"Image 2 added successfully! {image_result['output']['draft_id']}")

    print("\nTest: Adding image 3")
    image_result = add_image_impl(
        draft_id=image_result['output']['draft_id'],
        image_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_image_v2/d6e33c84d7554146a25b1093b012838b_0.png?x-oss-process=image/resize,w_500/watermark,image_aW1nL3dhdGVyMjAyNDExMjkwLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSxtX2ZpeGVkLHdfMTQ1LGhfMjU=,t_80,g_se,x_10,y_10/format,webp",
        width=480,
        height=480,
        start=10,
        end=15.0,
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main_2",  # Use different track name
        mask_type="Circle",  # Add circular mask
        mask_center_x=0.5,  # Mask center X coordinate (0.5 means centered)
        mask_center_y=0.5,  # Mask center Y coordinate (0.5 means centered)
        mask_size=0.8,  # Mask size (0.8 means 80%)
        mask_feather=0.1  # Mask feathering (0.1 means 10%)
    )
    print(f"Image 3 added successfully! {image_result['output']['draft_id']}")
    print(save_draft_impl(image_result['output']['draft_id'], draft_folder))

def test_mask_02():
    """Test adding videos to different tracks"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    video_url = "https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_video/092faf3c94244973ab752ee1280ba76f.mp4?spm=5176.29623064.0.0.41ed26d6cBOhV3&file=092faf3c94244973ab752ee1280ba76f.mp4" # Replace with actual video URL
    draft_id = None  # Initialize draft_id
    
    # Add video to first track
    video_result = add_video_impl(
        draft_id=draft_id,  # Pass in draft_id
        video_url=video_url,
        width=1920,
        height=1080,
        start=0,
        end=5.0, # Use first 5 seconds of video
        target_start=0,
        track_name="main_video_track"
    )
    draft_id = video_result['output']['draft_id']  # Update draft_id
    print(f"First video addition result: {video_result}")
    
    # Add video to second track
    video_result = add_video_impl(
        draft_id=draft_id,  # Use previous draft_id
        video_url=video_url,
        width=1920,
        height=1080,
        start=0,
        end=5.0, # Use first 5 seconds of video
        target_start=0,
        track_name="main_video_track_2",  # Use different track name
        speed=1.0,  # Change playback speed
        scale_x=0.5,  # Reduce video width
        transform_y=0.5  # Place video at bottom of screen
    )
    draft_id = video_result['output']['draft_id']  # Update draft_id
    print(f"Second video addition result: {video_result}")
    
    # Third time add video to another track with circular mask
    video_result = add_video_impl(
        draft_id=draft_id,  # Use previous draft_id
        video_url=video_url,
        width=1920,
        height=1080,
        start=0,
        end=5.0, # Use first 5 seconds of video
        target_start=0,
        track_name="main_video_track_3",  # Use third track
        speed=1.5,  # Faster playback speed
        scale_x=0.3,  # Smaller video width
        transform_y=-0.5,  # Place video at top of screen
        mask_type="Circle",  # Add circular mask
        mask_center_x=0.5,  # Mask center X coordinate
        mask_center_y=0.5,  # Mask center Y coordinate
        mask_size=0.8,  # Mask size
        mask_feather=0.1  # Mask feathering
    )
    draft_id = video_result['output']['draft_id']  # Update draft_id
    print(f"Third video addition result: {video_result}")
    
    # Finally save and upload draft
    save_result = save_draft_impl(draft_id, draft_folder)
    print(f"Draft save result: {save_result}")


def test_audio01():
    """Test adding audio"""
    # draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    draft_folder = "/Users/sunguannan/Movies/CapCut/User Data/Projects/com.lveditor.draft"

    print("\nTest: Adding audio")
    audio_result = add_audio_track(
        audio_url="https://lf3-lv-music-tos.faceu.com/obj/tos-cn-ve-2774/oYACBQRCMlWBIrZipvQZhI5LAlUFYii0RwEPh",
        start=4,
        end=5,
        target_start=15,
        volume=0.8,
        speed=1.0,
        track_name="main_audio101",
        # effect_type="麦霸",
        effect_type="Tremble",
        effect_params=[90.0, 50.0]
    )
    print(f"Audio addition result: {audio_result}")
    print(save_draft_impl(audio_result['output']['draft_id'], draft_folder))


def test_audio02():
    """Test adding multiple audio segments"""
    # draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    draft_folder = "/Users/sunguannan/Movies/CapCut/User Data/Projects/com.lveditor.draft"

    print("\nTest: Adding audio 1")
    audio_result = add_audio_track(
        audio_url="https://lf3-lv-music-tos.faceu.com/obj/tos-cn-ve-2774/oYACBQRCMlWBIrZipvQZhI5LAlUFYii0RwEPh",
        start=4,
        end=5,
        target_start=0,
        volume=0.8,
        speed=1.0,
        track_name="main_audio101",
        # effect_type="麦霸",
        effect_type="Tremble",
        effect_params=[90.0, 50.0]
    )
    print(f"Audio addition result 1: {audio_result}")

    print("\nTest: Adding audio 2")
    audio_result = add_audio_track(
        draft_id=audio_result['output']['draft_id'],
        audio_url="https://lf3-lv-music-tos.faceu.com/obj/tos-cn-ve-2774/oYACBQRCMlWBIrZipvQZhI5LAlUFYii0RwEPh",
        start=4,
        end=5,
        target_start=1.5,
        volume=0.8,
        speed=1.0,
        track_name="main_audio101",
        # effect_type="麦霸",
        effect_type="Tremble",
        effect_params=[90.0, 50.0]
    )
    print(f"Audio addition result 2: {audio_result}")
    print(save_draft_impl(audio_result['output']['draft_id'], draft_folder))


def test_audio03():
    """Test adding audio in a loop"""
    # draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    draft_folder = "/Users/sunguannan/Movies/CapCut/User Data/Projects/com.lveditor.draft"

    draft_id = None  # Initialize draft_id
    
    for i in range(10):
        target_start = i * 1.5  # Increment by 1.5 seconds each time
        
        audio_result = add_audio_track(
            audio_url="https://lf3-lv-music-tos.faceu.com/obj/tos-cn-ve-2774/oYACBQRCMlWBIrZipvQZhI5LAlUFYii0RwEPh",
            start=4,
            end=5,
            target_start=target_start,
            volume=0.8,
            speed=1.0,
            track_name="main_audio101",
            # effect_type="麦霸",
            effect_type="Tremble",
            effect_params=[90.0, 50.0],
            draft_id=draft_id  # Pass the previous draft_id (None for the first time)
        )
        
        draft_id = audio_result['output']['draft_id']  # Update draft_id
        print(f"Audio addition result {i+1}: {audio_result}")
    
    # Finally save and upload draft
    save_result = save_draft_impl(draft_id, draft_folder)
    print(f"Draft save result: {save_result}")


def test_audio04():
    """Test adding audio to different tracks"""
    # draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    draft_folder = "/Users/sunguannan/Movies/CapCut/User Data/Projects/com.lveditor.draft"

    print("\nTest: Adding audio 1")
    audio_result = add_audio_track(
        audio_url="https://lf3-lv-music-tos.faceu.com/obj/tos-cn-ve-2774/oYACBQRCMlWBIrZipvQZhI5LAlUFYii0RwEPh",
        start=4,
        end=5,
        target_start=0,
        volume=0.8,
        speed=1.0,
        track_name="main_audio101",
        # effect_type="麦霸",
        effect_type="Tremble",
        effect_params=[90.0, 50.0]
    )
    print(f"Audio addition result 1: {audio_result}")

    print("\nTest: Adding audio 2")
    audio_result = add_audio_track(
        draft_id=audio_result['output']['draft_id'],
        audio_url="https://lf3-lv-music-tos.faceu.com/obj/tos-cn-ve-2774/oYACBQRCMlWBIrZipvQZhI5LAlUFYii0RwEPh",
        start=4,
        end=5,
        target_start=1.5,
        volume=0.8,
        speed=1.0,
        track_name="main_audio102",  # Use different track name
        # effect_type="麦霸",
        effect_type="Tremble",
        effect_params=[90.0, 50.0]
    )
    print(f"Audio addition result 2: {audio_result}")
    query_draft_status_impl_polling(audio_result['output']['draft_id'])
    save_draft_impl(audio_result['output']['draft_id'], draft_folder)

def add_subtitle_impl(srt, draft_id=None, time_offset=0.0, font_size=5.0,
                    bold=False, italic=False, underline=False, font_color="#ffffff",
                    transform_x=0.0, transform_y=0.0, scale_x=1.0, scale_y=1.0,
                    vertical=False, track_name="subtitle", alpha=1,
                    border_alpha=1.0, border_color="#000000", border_width=0.0,
                    background_color="#000000", background_style=1, background_alpha=0.0,
                    rotation=0.0, width=1080, height=1920):
    """API wrapper for add_subtitle service"""
    data = {
        "license_key": LICENSE_KEY,  # Using trial version license key
        "srt": srt,  # Modified parameter name to match server side
        "draft_id": draft_id,
        "time_offset": time_offset,
        "font_size": font_size,
        "bold": bold,
        "italic": italic,
        "underline": underline,
        "font_color": font_color,
        "transform_x": transform_x,
        "transform_y": transform_y,
        "scale_x": scale_x,
        "scale_y": scale_y,
        "vertical": vertical,
        "track_name": track_name,
        "alpha": alpha,
        "border_alpha": border_alpha,
        "border_color": border_color,
        "border_width": border_width,
        "background_color": background_color,
        "background_style": background_style,
        "background_alpha": background_alpha,
        "rotation": rotation,
        "width": width,
        "height": height
    }
    return make_request("add_subtitle", data)

def save_draft_impl(draft_id, draft_folder):
    """API wrapper for save_draft service"""
    data = {
        "license_key": LICENSE_KEY,  # Using trial version license key
        "draft_id": draft_id,
        "draft_folder": draft_folder
    }
    return make_request("save_draft", data)

def query_script_impl(draft_id):
    """API wrapper for query_script service"""
    data = {
        "draft_id": draft_id
    }
    return make_request("query_script", data)

def query_draft_status_impl(task_id):
    """API wrapper for query_draft_status service"""
    data = {
        "license_key": LICENSE_KEY,  # Using trial version license key
        "task_id": task_id
    }
    return make_request("query_draft_status", data)
    
def query_draft_status_impl_polling(task_id, timeout=300, callback=None):
    """
    Poll for draft download status, implemented with async thread to avoid blocking the main thread
    
    :param task_id: task ID returned by save_draft_impl
    :param timeout: timeout in seconds, default 5 minutes
    :param callback: optional callback function called when task completes, fails or times out, with final status as parameter
    :return: tuple of thread object and result container, can be used to get results later
    """
    # Create result container to store final result
    result_container = {"result": None}
    
    def _polling_thread():
        start_time = time.time()
        print(f"Starting to query status for task {task_id}...")
        
        while True:
            try:
                # Get current task status
                task_status = query_draft_status_impl(task_id).get("output", {})
                
                # Print current status
                status = task_status.get("status", "unknown")
                message = task_status.get("message", "")
                progress = task_status.get("progress", 0)
                print(f"Current status: {status}, progress: {progress}%, message: {message}")
                
                # Check if completed or failed
                if status == "completed":
                    print(f"Task completed! Draft URL: {task_status.get('draft_url', 'Not provided')}")
                    result_container["result"] = task_status.get('draft_url', 'Not provided')
                    if callback:
                        callback(task_status.get('draft_url', 'Not provided'))
                    break
                elif status == "failed":
                    print(f"Task failed: {message}")
                    result_container["result"] = task_status
                    if callback:
                        callback(task_status)
                    break
                elif status == "not_found":
                    print(f"Task does not exist: {task_id}")
                    result_container["result"] = task_status
                    if callback:
                        callback(task_status)
                    break
                
                # Check if timed out
                elapsed_time = time.time() - start_time
                if elapsed_time > timeout:
                    print(f"Query timed out, waited {timeout} seconds")
                    result_container["result"] = task_status
                    if callback:
                        callback(task_status)
                    break
            except Exception as e:
                # Catch all exceptions to prevent thread crash
                print(f"Exception occurred during query: {e}")
                time.sleep(1)  # Wait 1 second before retrying after error
                continue
            
            # Wait 1 second before querying again
            time.sleep(1)
    
    # Create and start thread
    thread = threading.Thread(target=_polling_thread)
    # thread.daemon = True  # Set as daemon thread, automatically terminates when main thread ends
    thread.start()
    
    # Return thread object and result container for external code to get results
    return thread, result_container

def test_subtitle():
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"

    # Test case: Add text subtitles
    print("\nTest: Adding text subtitles")
    text_result = add_subtitle_impl(
        srt="1\n00:00:00,000 --> 00:00:04,433\nHello, I am the CapCut draft assistant developed by Sun Guannan.\n\n2\n00:00:04,433 --> 00:00:11,360\nI specialize in combining audio, video, and image materials to create CapCut drafts.\n",
        font_size=8.0,
        bold=True,
        italic=True,
        underline=True,
        font_color="#FF0000",
        transform_y=0,
        transform_x=0.4,
        time_offset=42,
        scale_x=1.0,
        scale_y=2.0,
        vertical=True,
        # Add background color parameters
        background_color="#FFFF00",  # Yellow background
        background_style=1,  # Style 1 means rectangular background
        background_alpha=0.7,  # 70% opacity
        # Add border parameters
        border_color="#0000FF",  # Blue border
        border_width=20.0,  # Border width 2
        border_alpha=1.0  # Fully opaque
    )
    print(f"Text addition result: {text_result}")
    
    # Save draft
    if text_result.get('success') and text_result.get('output'):
        save_result = save_draft_impl(text_result['output']['draft_id'], draft_folder)
        print(f"Draft save result: {save_result}")

def test01():
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    # draft_folder = "/Users/sunguannan/Movies/CapCut/User Data/Projects/com.lveditor.draft"

    # Combined test
    print("\nTest 2: Add audio")
    audio_result = add_audio_track(
        audio_url = "https://lf3-lv-music-tos.faceu.com/obj/tos-cn-ve-2774/oYACBQRCMlWBIrZipvQZhI5LAlUFYii0RwEPh",
        start=4,
        end=5,
        target_start=2,
        volume=0.8,
        speed=1.0,
        track_name="main_audio100",
        effect_type="Tremble",
        effect_params=[90.0, 50.0]
    )
    print(f"Audio addition result 1: {audio_result}")

    audio_result = add_audio_track(
        draft_id=audio_result['output']['draft_id'],
        audio_url = "https://lf3-lv-music-tos.faceu.com/obj/tos-cn-ve-2774/oYACBQRCMlWBIrZipvQZhI5LAlUFYii0RwEPh",
        start=4,
        end=5,
        target_start=4,
        volume=0.8,
        speed=1.0,
        track_name="main_audio100",
        effect_type="Tremble",
        effect_params=[90.0, 50.0]
    )
    print(f"Audio addition result 2: {audio_result}")

    audio_result = add_audio_track(
        draft_id=audio_result['output']['draft_id'],
        audio_url = "https://lf3-lv-music-tos.faceu.com/obj/tos-cn-ve-2774/oYACBQRCMlWBIrZipvQZhI5LAlUFYii0RwEPh",
        start=4,
        end=5,
        target_start=6,
        volume=0.8,
        speed=1.0,
        track_name="main_audio101",
        effect_type="Tremble",
        effect_params=[90.0, 50.0]
    )
    print(f"Audio addition result 3: {audio_result}")

    # Test case 1: Basic text addition
    text_result = add_text_impl(
        draft_folder=draft_folder,
        text="Test Text 1",
        draft_id=audio_result['output']['draft_id'],
        start=0,
        end=3,
        font="思源中宋",  # Use Source Han Serif font
        font_color="#FF0000",  # Red
        track_name="main_text",
        transform_y=0.8,
        transform_x=0.5,
        font_size=30.0
    )
    print("Test case 1 (Basic text) successful:", text_result)

    # Test case 2: Vertical text
    result2 = add_text_impl(
        draft_id=text_result['output']['draft_id'],
        text="Vertical Text Test",
        start=3,
        end=6,
        font="云书法三行魏碑体",
        font_color="#00FF00",  # Green
        font_size=8.0,
        track_name="main_text",
        vertical=True,  # Enable vertical text
        transform_y=-0.5,
        outro_animation='Fade_Out'
    )
    print("Test case 2 (Vertical text) successful:", result2)

    print("Test completed")
    # Test adding image
    image_result = add_image_impl(
        draft_id=result2['output']['draft_id'],  # Replace with actual draft ID
        image_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_image_v2/d6e33c84d7554146a25b1093b012838b_0.png?x-oss-process=image/resize,w_500/watermark,image_aW1nL3dhdGVyMjAyNDExMjkwLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSxtX2ZpeGVkLHdfMTQ1LGhfMjU=,t_80,g_se,x_10,y_10/format,webp",  # Replace with actual image URL
        width=480,
        height=480,
        start = 0,
        end=5.0,  # Display for 5 seconds
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main"
    )
    print("Image added successfully!")


    # Test adding image
    image_result = add_image_impl(
        draft_id=result2['output']['draft_id'],  # Replace with actual draft ID
        image_url="http://gips0.baidu.com/it/u=3602773692,1512483864&fm=3028&app=3028&f=JPEG&fmt=auto?w=960&h=1280",  # Replace with actual image URL
        width=480,
        height=480,
        start = 0,
        end=5.0,  # Display for 5 seconds
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main_2"
    )
    print("Image added successfully!")

    image_result = add_image_impl(
        draft_id=image_result['output']['draft_id'],  # Replace with actual draft ID
        image_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_image_v2/d6e33c84d7554146a25b1093b012838b_0.png?x-oss-process=image/resize,w_500/watermark,image_aW1nL3dhdGVyMjAyNDExMjkwLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSxtX2ZpeGVkLHdfMTQ1LGhfMjU=,t_80,g_se,x_10,y_10/format,webp",  # Replace with actual image URL
        width=480,
        height=480,
        start = 5,
        end=10.0,  # Display for 5 seconds
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main"
    )
    print("Image 2 added successfully!")

    # Test adding video keyframe
    print("\nTest: Add video keyframe")
    keyframe_result = add_video_keyframe_impl(
        draft_id=image_result['output']['draft_id'],  # Use existing draft ID
        track_name="main",
        property_type="position_y",  # Test opacity
        time=1.5,  # Add keyframe at 3.5 seconds
        value="0.2"  # Move 300px
    )
    print(f"Keyframe addition result: {keyframe_result}")

    print("\nTest: Add video keyframe")
    keyframe_result = add_video_keyframe_impl(
        draft_id=image_result['output']['draft_id'],  # Use existing draft ID
        track_name="main",
        property_type="position_y",  # Test opacity
        time=3.5,  # Add keyframe at 3.5 seconds
        value="0.4"  # Move 300px
    )
    print(f"Keyframe addition result: {keyframe_result}")
    
    query_draft_status_impl_polling(keyframe_result['output']['draft_id'])
    save_draft_impl(keyframe_result['output']['draft_id'], draft_folder)

def test02():
    # draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    draft_folder = "/Users/sunguannan/Movies/CapCut/User Data/Projects/com.lveditor.draft"

    # Combined test
    print("\nTest 2: Add audio")
    audio_result = add_audio_track(
        audio_url = "https://lf3-lv-music-tos.faceu.com/obj/tos-cn-ve-2774/oYACBQRCMlWBIrZipvQZhI5LAlUFYii0RwEPh",
        start=4,
        end=5,
        target_start=2,
        volume=0.8,
        speed=1.0,
        track_name="main_audio100",
        effect_type = "Big_House",
        effect_params = [50.0]
    )
    print(f"Audio addition result 1: {audio_result}")

    audio_result = add_audio_track(
        draft_id=audio_result['output']['draft_id'],
        audio_url = "https://lf3-lv-music-tos.faceu.com/obj/tos-cn-ve-2774/oYACBQRCMlWBIrZipvQZhI5LAlUFYii0RwEPh",
        start=4,
        end=5,
        target_start=4,
        volume=0.8,
        speed=1.0,
        track_name="main_audio100",
        effect_type = "Big_House",
        effect_params = [50.0]
    )
    print(f"Audio addition result 2: {audio_result}")

    audio_result = add_audio_track(
        draft_id=audio_result['output']['draft_id'],
        audio_url = "https://lf3-lv-music-tos.faceu.com/obj/tos-cn-ve-2774/oYACBQRCMlWBIrZipvQZhI5LAlUFYii0RwEPh",
        start=4,
        end=5,
        target_start=6,
        volume=0.8,
        speed=1.0,
        track_name="main_audio101",
        effect_type = "Big_House",
        effect_params = [50.0]
    )
    print(f"Audio addition result 3: {audio_result}")

    # Test case 1: Basic text addition
    text_result = add_text_impl(
        draft_folder=draft_folder,
        text="Test Text 1",
        draft_id=audio_result['output']['draft_id'],
        start=0,
        end=3,
        font="思源中宋",  # Use Source Han Serif font
        font_color="#FF0000",  # Red
        track_name="main_text",
        transform_y=0.8,
        transform_x=0.5,
        font_size=30.0
    )
    print("Test case 1 (Basic text) successful:", text_result)

    # Test case 2: Vertical text
    result2 = add_text_impl(
        draft_id=text_result['output']['draft_id'],
        text="Vertical Text Test",
        start=3,
        end=6,
        font="云书法三行魏碑体",
        font_color="#00FF00",  # Green
        font_size=8.0,
        track_name="main_text",
        vertical=True,  # Enable vertical text
        transform_y=-0.5,
        outro_animation='Throw_Back'
    )
    print("Test case 2 (Vertical text) successful:", result2)

    print("Test completed")
    # Test adding image
    image_result = add_image_impl(
        draft_id=result2['output']['draft_id'],  # Replace with actual draft ID
        image_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_image_v2/d6e33c84d7554146a25b1093b012838b_0.png?x-oss-process=image/resize,w_500/watermark,image_aW1nL3dhdGVyMjAyNDExMjkwLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSxtX2ZpeGVkLHdfMTQ1LGhfMjU=,t_80,g_se,x_10,y_10/format,webp",  # Replace with actual image URL
        width=480,
        height=480,
        start = 0,
        end=5.0,  # Display for 5 seconds
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main"
    )
    print("Image added successfully!")


    # Test adding image
    image_result = add_image_impl(
        draft_id=result2['output']['draft_id'],  # Replace with actual draft ID
        image_url="http://gips0.baidu.com/it/u=3602773692,1512483864&fm=3028&app=3028&f=JPEG&fmt=auto?w=960&h=1280",  # Replace with actual image URL
        width=480,
        height=480,
        start = 0,
        end=5.0,  # Display for 5 seconds
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main_2"
    )
    print("Image added successfully!")

    image_result = add_image_impl(
        draft_id=image_result['output']['draft_id'],  # Replace with actual draft ID
        image_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_image_v2/d6e33c84d7554146a25b1093b012838b_0.png?x-oss-process=image/resize,w_500/watermark,image_aW1nL3dhdGVyMjAyNDExMjkwLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSxtX2ZpeGVkLHdfMTQ1LGhfMjU=,t_80,g_se,x_10,y_10/format,webp",  # Replace with actual image URL
        width=480,
        height=480,
        start = 5,
        end=10.0,  # Display for 5 seconds
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main"
    )
    print("Image 2 added successfully!")

    # Test adding video keyframe
    print("\nTest: Add video keyframe")
    keyframe_result = add_video_keyframe_impl(
        draft_id=image_result['output']['draft_id'],  # Use existing draft ID
        track_name="main",
        property_type="position_y",  # Test opacity
        time=1.5,  # Add keyframe at 3.5 seconds
        value="0.2"  # Move 300px
    )
    print(f"Keyframe addition result: {keyframe_result}")

    print("\nTest: Add video keyframe")
    keyframe_result = add_video_keyframe_impl(
        draft_id=image_result['output']['draft_id'],  # Use existing draft ID
        track_name="main",
        property_type="position_y",  # Test opacity
        time=3.5,  # Add keyframe at 3.5 seconds
        value="0.4"  # Move 300px
    )
    print(f"Keyframe addition result: {keyframe_result}")
    
    query_draft_status_impl_polling(keyframe_result['output']['draft_id'])
    save_draft_impl(keyframe_result['output']['draft_id'], draft_folder)

def test_video_track01():
    """Test adding video track"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    video_url = "https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_video/092faf3c94244973ab752ee1280ba76f.mp4?spm=5176.29623064.0.0.41ed26d6cBOhV3&file=092faf3c94244973ab752ee1280ba76f.mp4" # Replace with actual video URL

    print("\nTest: Add video track")
    video_result = add_video_impl(
        video_url=video_url,
        width=1920,
        height=1080,
        start=0,
        end=5.0, # Cut the first 5 seconds of the video
        target_start=0,
        track_name="main_video_track"
    )
    print(f"Video track addition result: {video_result}")

    if video_result and 'output' in video_result and 'draft_id' in video_result['output']:
        draft_id = video_result['output']['draft_id']
        print(f"Save draft: {save_draft_impl(draft_id, draft_folder)}")
    else:
        print("Unable to get draft ID, skipping save operation.")


def test_video_track02():
    """Test adding video tracks in a loop"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    video_url = "https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_video/092faf3c94244973ab752ee1280ba76f.mp4?spm=5176.29623064.0.0.41ed26d6cBOhV3&file=092faf3c94244973ab752ee1280ba76f.mp4" # Replace with actual video URL
    draft_id = None  # Initialize draft_id
    
    for i in range(5):
        target_start = i * 5  # Increment by 5 seconds each time
        
        video_result = add_video_impl(
            draft_id=draft_id,  # Pass in draft_id
            video_url=video_url,
            width=1920,
            height=1080,
            start=0,
            end=5.0, # Cut the first 5 seconds of the video
            target_start=target_start,
            track_name="main_video_track"
        )
        draft_id = video_result['output']['draft_id']  # Update draft_id
        print(f"Video addition result {i+1}: {video_result}")
    
    # Finally save and upload the draft
    save_result = save_draft_impl(draft_id, draft_folder)
    print(f"Draft save result: {save_result}")


def test_video_track03():
    """Test adding videos to different tracks"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    video_url = "https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_video/092faf3c94244973ab752ee1280ba76f.mp4?spm=5176.29623064.0.0.41ed26d6cBOhV3&file=092faf3c94244973ab752ee1280ba76f.mp4" # Replace with actual video URL
    draft_id = None  # Initialize draft_id
    
    # Add video to the first track
    video_result = add_video_impl(
        draft_id=draft_id,  # Pass in draft_id
        video_url=video_url,
        width=1920,
        height=1080,
        start=0,
        end=5.0, # Cut the first 5 seconds of the video
        target_start=0,
        track_name="main_video_track"
    )
    draft_id = video_result['output']['draft_id']  # Update draft_id
    print(f"First video addition result: {video_result}")
    
    # Add video to the second track
    video_result = add_video_impl(
        draft_id=draft_id,  # Use previous draft_id
        video_url=video_url,
        width=1920,
        height=1080,
        start=0,
        end=5.0, # Cut the first 5 seconds of the video
        target_start=0,
        track_name="main_video_track_2",  # Use different track name
        speed=1.0,  # Change playback speed
        scale_x=0.5,  # Reduce video width
        transform_y=0.5  # Position video at bottom of screen
    )
    draft_id = video_result['output']['draft_id']  # Update draft_id
    print(f"Second video addition result: {video_result}")
    
    # Third time add video to another track
    video_result = add_video_impl(
        draft_id=draft_id,  # Use previous draft_id
        video_url=video_url,
        width=1920,
        height=1080,
        start=0,
        end=5.0, # Cut the first 5 seconds of the video
        target_start=0,
        track_name="main_video_track_3",  # Use third track
        speed=1.5,  # Faster playback speed
        scale_x=0.3,  # Smaller video width
        transform_y=-0.5  # Position video at top of screen
    )
    draft_id = video_result['output']['draft_id']  # Update draft_id
    print(f"Third video addition result: {video_result}")
    
    # Finally save and upload the draft
    save_result = save_draft_impl(draft_id, draft_folder)
    print(f"Draft save result: {save_result}")

def test_video_track04():
    """Test adding video track"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    video_url = "https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_video/092faf3c94244973ab752ee1280ba76f.mp4?spm=5176.29623064.0.0.41ed26d6cBOhV3&file=092faf3c94244973ab752ee1280ba76f.mp4" # Replace with actual video URL

    print("\nTest: Add video track")
    video_result = add_video_impl(
        video_url='https://p26-bot-workflow-sign.byteimg.com/tos-cn-i-mdko3gqilj/07bf6797a1834d75beb05c63293af204.mp4~tplv-mdko3gqilj-image.image?rk3s=81d4c505&x-expires=1782141919&x-signature=2ETX83Swh%2FwKzHeWB%2F9oGq9vqt4%3D&x-wf-file_name=output-997160b5.mp4'
    )
    print(f"Video track addition result: {video_result}")

    print("\nTest: Add video track")
    video_result = add_video_impl(
        video_url='https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_video/092faf3c94244973ab752ee1280ba76f.mp4?spm=5176.29623064.0.0.41ed26d6cBOhV3&file=092faf3c94244973ab752ee1280ba76f.mp4',
        draft_id=video_result['output']['draft_id'],  # Use existing draft ID
        target_start=19.84
    )
    print(f"Video track addition result: {video_result}")
    if video_result and 'output' in video_result and 'draft_id' in video_result['output']:
        draft_id = video_result['output']['draft_id']
        print(f"Save draft: {save_draft_impl(draft_id, draft_folder)}")
    else:
        print("Unable to get draft ID, skipping save operation.")

def test_keyframe():
    """Test adding keyframes"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    draft_id = None  # Initialize draft_id
    
    print("\nTest: Add basic video track")
    video_result = add_video_impl(
        video_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_video/092faf3c94244973ab752ee1280ba76f.mp4?spm=5176.29623064.0.0.41ed26d6cBOhV3&file=092faf3c94244973ab752ee1280ba76f.mp4",
        width=1920,
        height=1080,
        start=0,
        end=10.0,
        target_start=0,
        track_name="main_video_track"
    )
    print("Video addition result:", video_result)
    
    if video_result.get('success') and video_result.get('output'):
        draft_id = video_result['output']['draft_id']
        print("Using existing draft_id:", draft_id)
    else:
        print("Unable to get draft ID, terminating test.")
        return

    print("\nTest: Add opacity keyframe")
    keyframe_result = add_video_keyframe_impl(
        draft_id=draft_id,
        track_name="main_video_track",
        property_type="alpha",
        time=2.0,
        value="1.0"
    )
    print("Opacity keyframe addition result:", keyframe_result)

    print("\nTest: Add position Y keyframe")
    keyframe_result = add_video_keyframe_impl(
        draft_id=draft_id,
        track_name="main_video_track",
        property_type="position_y",
        time=2.0,
        value="0.5"
    )
    print("Position Y keyframe addition result:", keyframe_result)

    print("\nTest: Add scale X keyframe")
    keyframe_result = add_video_keyframe_impl(
        draft_id=draft_id,
        track_name="main_video_track",
        property_type="position_y",
        time=4.0,
        value="-0.5"
    )
    print("Scale X keyframe addition result:", keyframe_result)

    print("\nFinal draft save")
    save_result = save_draft_impl(draft_id, draft_folder)
    print(f"Draft save result: {save_result}")

def test_keyframe_02():
    """Test adding keyframes - Batch adding to implement fade-in and zoom bounce effects"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    draft_id = None  # Initialize draft_id
    
    print("\nTest: Adding basic video track")
    video_result = add_video_impl(
        video_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_video/092faf3c94244973ab752ee1280ba76f.mp4?spm=5176.29623064.0.0.41ed26d6cBOhV3&file=092faf3c94244973ab752ee1280ba76f.mp4",
        width=1920,
        height=1080,
        start=0,
        end=10.0,
        target_start=0,
        track_name="main_video_track"
    )
    print("Video adding result:", video_result)
    
    if video_result.get('success') and video_result.get('output'):
        draft_id = video_result['output']['draft_id']
        print("Using existing draft_id:", draft_id)
    else:
        print("Unable to get draft ID, terminating test.")
        return

    print("\nTest: Batch adding opacity keyframes - Implementing fade-in effect")
    # Add opacity keyframes to implement fade-in effect from invisible to visible
    alpha_keyframe_result = add_video_keyframe_impl(
        draft_id=draft_id,
        track_name="main_video_track",
        property_types=["alpha", "alpha", "alpha", "alpha"],
        times=[0.0, 1.0, 2.0, 3.0],
        values=["0.0", "0.3", "0.7", "1.0"]
    )
    print("Opacity keyframe batch adding result:", alpha_keyframe_result)

    print("\nTest: Batch adding scale keyframes - Implementing zoom bounce effect")
    # Add uniform scale keyframes to implement zoom bounce effect
    scale_keyframe_result = add_video_keyframe_impl(
        draft_id=draft_id,
        track_name="main_video_track",
        property_types=["uniform_scale", "uniform_scale", "uniform_scale", "uniform_scale", "uniform_scale"],
        times=[0.0, 1.5, 3.0, 4.5, 6.0],
        values=["0.8", "1.3", "1.0", "1.2", "1.0"]
    )
    print("Scale keyframe batch adding result:", scale_keyframe_result)

    print("\nTest: Batch adding position Y keyframes - Implementing up and down floating effect")
    # Add position Y keyframes to implement up and down floating effect
    position_y_keyframe_result = add_video_keyframe_impl(
        draft_id=draft_id,
        track_name="main_video_track",
        property_types=["position_y", "position_y", "position_y", "position_y"],
        times=[2.0, 3.5, 5.0, 6.5],
        values=["0.0", "0.2", "-0.2", "0.0"]
    )
    print("Position Y keyframe batch adding result:", position_y_keyframe_result)

    print("\nFinal draft saving")
    save_result = save_draft_impl(draft_id, draft_folder)
    print(f"Draft saving result: {save_result}")

def test_subtitle_01():
    """Test adding text subtitles"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    
    print("\nTest 3: Adding text subtitles")
    text_result = add_subtitle_impl(
        srt="1\n00:00:00,000 --> 00:00:04,433\n你333好，我是孙关南开发的剪映草稿助手。\n\n2\n00:00:04,433 --> 00:00:11,360\n我擅长将音频、视频、图片素材拼接在一起剪辑输出剪映草稿。\n",
        font_size=8.0,
        bold=True,
        italic=True,
        underline=True,
        font_color="#FF0000",
        transform_y=0,
        transform_x=0.4,
        time_offset=42,
        scale_x=1.0,
        scale_y=2.0,
        vertical=True
    )
    print(f"Text adding result: {text_result}")
    
    if text_result.get('success') and text_result.get('output'):
        save_result = save_draft_impl(text_result['output']['draft_id'], draft_folder)
        print(f"Draft saving result: {save_result}")
    
    return text_result


def test_subtitle_02():
    """Test adding text subtitles via SRT URL"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    
    print("\nTest 3: Adding text subtitles (from URL)")
    text_result = add_subtitle_impl(
        srt="https://oss-oversea-bucket.oss-cn-hongkong.aliyuncs.com/dfd_srt_1748575460_kmtu56iu.srt?Expires=1748707452&OSSAccessKeyId=TMP.3Km5TL5giRLgDkc3CamKPcWZTmSrLVeRxPWxEisNB2CTymvUxrpX8VXzy5r99F6bJkwjwFM5d1RsiV3cF18iaMriAPtA1y&Signature=4JzB4YGiChsxcTFuvUyZ0v3MjMI%3D",
        font_size=8.0,
        bold=True,
        italic=True,
        underline=True,
        font_color="#FF0000",
        transform_y=0,
        transform_x=0.4,
        time_offset=42,
        scale_x=1.0,
        scale_y=2.0,
        vertical=True
    )
    print(f"Text adding result: {text_result}")
    
    if text_result.get('success') and text_result.get('output'):
        save_result = save_draft_impl(text_result['output']['draft_id'], draft_folder)
        print(f"Draft saving result: {save_result}")
    
    return text_result


def test_video():
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"

    print("\nTest: Adding video")
    video_result = add_video_impl(
        video_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_video/092faf3c94244973ab752ee1280ba76f.mp4?spm=5176.29623064.0.0.41ed26d6cBOhV3&file=092faf3c94244973ab752ee1280ba76f.mp4", # Replace with actual video URL
        start=0,
        end=5,
        width=1920,
        height=1080,
        track_name="main_video",
        transform_y=0.1,
        scale_x=0.8,
        scale_y=0.8,
        transform_x=0.1,
        speed=1.2,
        target_start=0,
        relative_index=0
    )
    print(f"Video adding result: {video_result}")

    # Save draft
    if video_result.get('success') and video_result.get('output'):
        query_draft_status_impl_polling(video_result['output']['draft_id'])
        save_draft_impl(video_result['output']['draft_id'], draft_folder)
        
def test_video_02():
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"

    print("\nTest: Adding video")
    video_result = add_video_impl(
        video_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_video/092faf3c94244973ab752ee1280ba76f.mp4?spm=5176.29623064.0.0.41ed26d6cBOhV3&file=092faf3c94244973ab752ee1280ba76f.mp4", # Replace with actual video URL
        start=0,
        end=5,
        width=1920,
        height=1080,
        track_name="main_video",
        transform_y=0.1,
        scale_x=0.8,
        scale_y=0.8,
        transform_x=0.1,
        speed=1.2,
        target_start=0,
        relative_index=0
    )
    print(f"Video adding result: {video_result}")

    video_result = add_video_impl(
        video_url="https://videos.pexels.com/video-files/3129769/3129769-hd_1280_720_30fps.mp4", # Replace with actual video URL
        draft_id=video_result['output']['draft_id'],
        start=0,
        end=5,
        width=1920,
        height=1080,
        track_name="main_video_2",
        transform_y=0.1,
        scale_x=0.8,
        scale_y=0.8,
        transform_x=0.1,
        speed=1.2,
        target_start=0,
        relative_index=0
    )
    video_result = add_video_impl(
        video_url="https://videos.pexels.com/video-files/3129769/3129769-uhd_3840_2160_30fps.mp4", # 替换为实际的视频URL
        draft_id=video_result['output']['draft_id'],
        start=0,
        end=5,
        width=1920,
        height=1080,
        track_name="main_video_3",
        transform_y=0.1,
        scale_x=0.8,
        scale_y=0.8,
        transform_x=0.1,
        speed=1.2,
        target_start=0,
        relative_index=0
    )
    video_result = add_video_impl(
        video_url="https://videos.pexels.com/video-files/3129769/3129769-sd_426_240_30fps.mp4", # 替换为实际的视频URL
        draft_id=video_result['output']['draft_id'],
        start=0,
        end=5,
        width=1920,
        height=1080,
        track_name="main_video_4",
        transform_y=0.1,
        scale_x=0.8,
        scale_y=0.8,
        transform_x=0.1,
        speed=1.2,
        target_start=0,
        relative_index=0
    )
    video_result = add_video_impl(
        video_url="https://videos.pexels.com/video-files/3129769/3129769-sd_640_360_30fps.mp4", # 替换为实际的视频URL
        draft_id=video_result['output']['draft_id'],
        start=0,
        end=5,
        width=1920,
        height=1080,
        track_name="main_video_5",
        transform_y=0.1,
        scale_x=0.8,
        scale_y=0.8,
        transform_x=0.1,
        speed=1.2,
        target_start=0,
        relative_index=0
    )
    video_result = add_video_impl(
        video_url="https://videos.pexels.com/video-files/3129769/3129769-uhd_2560_1440_30fps.mp4", # 替换为实际的视频URL
        draft_id=video_result['output']['draft_id'],
        start=0,
        end=5,
        width=1920,
        height=1080,
        track_name="main_video_6",
        transform_y=0.1,
        scale_x=0.8,
        scale_y=0.8,
        transform_x=0.1,
        speed=1.2,
        target_start=0,
        relative_index=0
    )

    if video_result.get('success') and video_result.get('output'):
        print(json.loads(query_script_impl(video_result['output']['draft_id'])['output']))
        # query_draft_status_impl_polling(video_result['output']['draft_id'])
        # save_draft_impl(video_result['output']['draft_id'], draft_folder)
   
def test_stiker_01():
    """Test adding stickers"""
    # Add stickers, test various parameters
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    result = add_sticker_impl(
        resource_id="7107529669750066445",
        start=1.0,
        end=4.0,
        transform_y=0.3,      # Move up
        transform_x=-0.2,     # Move left
        alpha=0.8,            # Set transparency
        rotation=45.0,        # Rotate 45 degrees
        scale_x=1.5,          # Horizontal scale 1.5x
        scale_y=1.5,          # Vertical scale 1.5x
        flip_horizontal=True  # Horizontal flip
    )
    print(f"Sticker adding result: {save_draft_impl(result['output']['draft_id'], draft_folder)}")

def test_stiker_02():
    """Test adding stickers"""
    # Add stickers, test various parameters
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    result = add_sticker_impl(
        resource_id="7107529669750066445",
        start=1.0,
        end=4.0,
        transform_y=0.3,      # Move up
        transform_x=-0.2,     # Move left
        alpha=0.8,            # Set transparency
        rotation=45.0,        # Rotate 45 degrees
        scale_x=1.5,          # Horizontal scale 1.5x
        scale_y=1.5,          # Vertical scale 1.5x
        flip_horizontal=True  # Horizontal flip
    )
    result = add_sticker_impl(
        resource_id="7107529669750066445",
        draft_id=result['output']['draft_id'],
        start=5.0,
        end=10.0,
        transform_y=-0.3,     # Move up
        transform_x=0.5,      # Move left
        alpha=0.1,            # Set transparency
        rotation=30.0,        # Rotate 30 degrees
        scale_x=1.5,          # Horizontal scale 1.5x
        scale_y=1.2,          # Vertical scale 1.2x
    )
    print(f"Sticker adding result: {save_draft_impl(result['output']['draft_id'], draft_folder)}")

def test_stiker_03():
    """Test adding stickers"""
    # Add stickers, test various parameters
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    result = add_sticker_impl(
        resource_id="7107529669750066445",
        start=1.0,
        end=4.0,
        transform_y=0.3,      # Move up
        transform_x=-0.2,     # Move left
        alpha=0.8,            # Set transparency
        rotation=45.0,        # Rotate 45 degrees
        scale_x=1.5,          # Horizontal scale 1.5x
        scale_y=1.5,          # Vertical scale 1.5x
        flip_horizontal=True, # Horizontal flip
        track_name="stiker_main",
        relative_index=999
    )
    result = add_sticker_impl(
        resource_id="7107529669750066445",
        draft_id=result['output']['draft_id'],
        start=5.0,
        end=10.0,
        transform_y=-0.3,     # Move up
        transform_x=0.5,      # Move left
        alpha=0.1,            # Set transparency
        rotation=30.0,        # Rotate 30 degrees
        scale_x=1.5,          # Horizontal scale 1.5x
        scale_y=1.2,          # Vertical scale 1.2x
        track_name="stiker_main_2",
        relative_index=0
    )
    print(f"Sticker adding result: {save_draft_impl(result['output']['draft_id'], draft_folder)}")


def test_transition_01():
    """Test adding multiple images"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"

    print("\nTest: Adding image 1")
    image_result = add_image_impl(
        image_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_image_v2/d6e33c84d7554146a25b1093b012838b_0.png?x-oss-process=image/resize,w_500/watermark,image_aW1nL3dhdGVyMjAyNDExMjkwLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSxtX2ZpeGVkLHdfMTQ1LGhfMjU=,t_80,g_se,x_10,y_10/format,webp",
        width=480,
        height=480,
        start=0,
        end=5.0,
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main",
        transition="Dissolve",
        transition_duration=1.0
    )
    print(f"Image 1 added successfully! {image_result['output']['draft_id']}")
    
    print("\nTest: Adding image 2")
    image_result = add_image_impl(
        draft_id=image_result['output']['draft_id'],
        image_url="https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_image_v2/d6e33c84d7554146a25b1093b012838b_0.png?x-oss-process=image/resize,w_500/watermark,image_aW1nL3dhdGVyMjAyNDExMjkwLnBuZz94LW9zcy1wcm9jZXNzPWltYWdlL3Jlc2l6ZSxtX2ZpeGVkLHdfMTQ1LGhfMjU=,t_80,g_se,x_10,y_10/format,webp",
        width=480,
        height=480,
        start=5,
        end=10.0,
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main"
    )
    print(f"Image 2 added successfully! {image_result['output']['draft_id']}")
    print(save_draft_impl(image_result['output']['draft_id'], draft_folder))


def test_transition_02():
    """Test adding video tracks"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    video_url = "https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_video/092faf3c94244973ab752ee1280ba76f.mp4?spm=5176.29623064.0.0.41ed26d6cBOhV3&file=092faf3c94244973ab752ee1280ba76f.mp4" # Replace with actual video URL

    print("\nTest: Adding video track")
    video_result = add_video_impl(
        video_url=video_url,
        width=1920,
        height=1080,
        start=0,
        end=5.0, # Trim first 5 seconds of video
        target_start=0,
        track_name="main_video_track",
        transition="Dissolve",
        transition_duration=1.0
    )
    print(f"Video track adding result: {video_result}")

    print("\nTest: Adding video track")
    video_result = add_video_impl(
        video_url=video_url,
        draft_id=video_result['output']['draft_id'],
        width=1920,
        height=1080,
        start=0,
        end=5.0, # Trim first 5 seconds of video
        target_start=5.0,
        track_name="main_video_track"
    )
    print(f"Video track adding result: {video_result}")

    if video_result and 'output' in video_result and 'draft_id' in video_result['output']:
        draft_id = video_result['output']['draft_id']
        print(f"Saving draft: {save_draft_impl(draft_id, draft_folder)}")
    else:
        print("Unable to get draft ID, skipping save operation.")

def test_generate_image01():
    """Test adding image"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"

    print("\nTest: Adding image 1")
    image_result = generate_image_impl(
        prompt="An Asian style doodle person floating in rough sea waves labeled 'Job Market', throwing paper boats made of resumes that are sinking, with a bank account notification bubble showing low balance. Atmosphere: Lost, anxious, turbulent. Art style: Minimalist line art, black and white cartoon style, bold outlines, extremely thick lines, expressive emotions, simple doodle, monochromatic. Composition: Wide angle showing person in center of chaotic elements. Lighting: Harsh contrast.",
        width=1024,
        height=1024,
        start=0,
        end=5.0,
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main"
    )
    print(f"Image generated successfully! {image_result['output']['draft_id']}")
    print(save_draft_impl(image_result['output']['draft_id'], draft_folder))

def generate_speech_impl(texts, draft_id=None, audio_track_name=None, language="Chinese", 
                        speaker_id="爽快思思/Skye",azure_speaker_id=None, speed_ratio=1.0, start_offset=0.0,
                        end_padding=0.0, interval_time=0.5, volume=1.0, width=1080, height=1920,
                        add_subtitle=True, text_track_name=None, font="文轩体", 
                        font_color="#ffffff", font_size=8.0, transform_y=-0.8, transform_x=0,
                        vertical=False, font_alpha=1.0, border_alpha=1.0, border_color="#000000",
                        border_width=0.0, background_color="#000000", background_style=1,
                        background_alpha=0.0, bubble_effect_id=None, bubble_resource_id=None,
                        effect_effect_id=None, intro_animation=None, intro_duration=0.5,
                        outro_animation=None, outro_duration=0.5):
    """Generate TTS speech and add to draft API call"""
    data = {
        "license_key": LICENSE_KEY,  # Using trial version license key
        "texts": texts,
        "audio_track_name": audio_track_name,
        "language": language,
        "speaker_id": speaker_id,
        "azure_speaker_id": azure_speaker_id,
        "speed_ratio": speed_ratio,
        "start_offset": start_offset,
        "end_padding": end_padding,
        "interval_time": interval_time,
        "volume": volume,
        "width": width,
        "height": height,
        "add_subtitle": add_subtitle,
        "text_track_name": text_track_name,
        "font": font,
        "font_color": font_color,
        "font_size": font_size,
        "transform_y": transform_y,
        "transform_x": transform_x,
        "vertical": vertical,
        "font_alpha": font_alpha,
        "border_alpha": border_alpha,
        "border_color": border_color,
        "border_width": border_width,
        "background_color": background_color,
        "background_style": background_style,
        "background_alpha": background_alpha,
        "bubble_effect_id": bubble_effect_id,
        "bubble_resource_id": bubble_resource_id,
        "effect_effect_id": effect_effect_id,
        "intro_animation": intro_animation,
        "intro_duration": intro_duration,
        "outro_animation": outro_animation,
        "outro_duration": outro_duration
    }
    
    if draft_id:
        data["draft_id"] = draft_id
        
    return make_request("generate_speech", data)

def test_generate_image02():
    """Test adding image"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"

    print("\nTest: Adding image 1")
    image_result = generate_image_impl(
        prompt="A cat in the garden",
        width=1024,
        height=1024,
        start=0,
        end=5.0,
        transform_y=0.7,
        scale_x=2.0,
        scale_y=1.0,
        transform_x=0,
        track_name="main"
    )
    print("\nTest: Adding image 2")
    image_result = generate_image_impl(
        prompt="3 dogs running in the snow",
        draft_id=image_result['output']['draft_id'],
        width=576,
        height=1024,
        start=5.0,
        end=10.0,
        transform_y=-0.7,
        scale_x=2.0,
        scale_y=2.0,
        transform_x=0,
        track_name="main"
    )
    print(f"Image generated successfully! {image_result['output']['draft_id']}")
    print(save_draft_impl(image_result['output']['draft_id'], draft_folder))

@timing_decorator('TTS Speech Generation')
def test_speech_01():
    """Test TTS speech generation and subtitle addition"""
    draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"

    print("\nTest: Generate TTS speech and add subtitles")
    speech_result = generate_speech_impl(
        texts=["Hello everyone, welcome to my video", "Today we will discuss an interesting topic","What to do when your child doesn't want to go to school", "Hope you enjoy this content","Hello everyone, welcome to my video", "Today we will discuss an interesting topic","What to do when your child doesn't want to go to school", "Hope you enjoy this content","Hello everyone, welcome to my video", "Today we will discuss an interesting topic","What to do when your child doesn't want to go to school", "Hope you enjoy this content"],
        language="Chinese",
        draft_id="123",
        speaker_id="渊博小叔",
        azure_speaker_id="zh-CN-YunjianNeural",
        speed_ratio=1.0,
        start_offset=1.0,
        end_padding=1.0,
        interval_time=0.5,
        volume=0.8,
        width=1080,
        height=1920,
        add_subtitle=True,
        font="文轩体",
        font_color="#ffffff",
        font_size=8.0,
        transform_y=-0.8,
        transform_x=0,
        border_width=2.0,
        border_color="#000000",
        border_alpha=0.8
    )
    print(f"TTS speech generation result: {speech_result}")
    
    # if speech_result.get('success'):
    #     # Save draft
    #     save_result = save_draft_impl(speech_result['output']['draft_id'], draft_folder)
    #     print(f"Draft saving result: {save_result}")
    # else:
    #     print(f"TTS generation failed: {speech_result.get('error')}")

if __name__ == "__main__":
    # test01()
    # test02()
    # test_effect_01()  # Run effect test
    # test_audio01()
    # test_audio02()
    # test_audio03()
    # test_audio04()
    test_image01()
    # test_image02()
    # test_image03()
    # test_image04()
    # test_video()
    # test_video_02()
    # test_text()
    # test_video_track01()
    # test_video_track02()
    # test_video_track03()
    # test_video_track04()
    # test_keyframe()
    # test_keyframe_02()
    # test_subtitle_01()
    # test_subtitle_02()
    # test_subtitle()
    # test_stiker_01()
    # test_stiker_02()
    # test_stiker_03()
    # test_transition_01()
    # test_transition_02()
    # test_generate_image01()
    # test_generate_image02()
    # test_speech_01()
    # test_mask_01()
    # test_mask_02()