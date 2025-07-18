from fastapi import APIRouter
from app.schemas import AddVideoRequest, AddVideoKeyframeRequest
from app.controllers import add_video, add_video_keyframe

router = APIRouter(tags=["视频"])

@router.post('/add_video',operation_id='add_video')
async def add_video_route(request: AddVideoRequest):
    return await add_video(request)

@router.post('/add_video_keyframe',operation_id='add_video_keyframe')
async def add_video_keyframe_route(request: AddVideoKeyframeRequest):
    return await add_video_keyframe(request) 