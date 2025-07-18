from fastapi import APIRouter
from app.schemas import AddEffectRequest, AddStickerRequest
from app.controllers import add_effect, add_sticker

router = APIRouter(tags=["特效"])

@router.post('/add_effect',operation_id='add_effect')
async def add_effect_route(request: AddEffectRequest):
    return await add_effect(request)

@router.post('/add_sticker',operation_id='add_sticker')
async def add_sticker_route(request: AddStickerRequest):
    return await add_sticker(request) 