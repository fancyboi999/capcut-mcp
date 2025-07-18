from fastapi import APIRouter
from app.schemas import AddImageRequest
from app.controllers import add_image

router = APIRouter(tags=["图像"])

@router.post('/add_image',operation_id='add_image')
async def add_image_route(request: AddImageRequest):
    return await add_image(request) 