from fastapi import APIRouter
from app.schemas import AddTextRequest, AddSubtitleRequest
from app.controllers import add_text, add_subtitle

router = APIRouter(tags=["文本"])

@router.post('/add_text',operation_id='add_text')
async def add_text_route(request: AddTextRequest):
    return await add_text(request)

@router.post('/add_subtitle',operation_id='add_subtitle')
async def add_subtitle_route(request: AddSubtitleRequest):
    return await add_subtitle(request) 