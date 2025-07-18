from fastapi import APIRouter
from app.schemas import (
    CreateDraftRequest,
    SaveDraftRequest,
    QueryDraftStatusRequest,
    GenerateDraftUrlRequest,
    QueryScriptRequest
)
from app.controllers import (
    create_draft_service,
    save_draft,
    query_draft_status,
    generate_draft_url,
    query_script
)

router = APIRouter(tags=["草稿"])

@router.post('/create_draft',operation_id='create_draft')
async def create_draft_route(request: CreateDraftRequest):
    return await create_draft_service(request)

@router.post('/save_draft',operation_id='save_draft')
async def save_draft_route(request: SaveDraftRequest):
    return await save_draft(request)

@router.post('/query_draft_status',operation_id='query_draft_status')
async def query_draft_status_route(request: QueryDraftStatusRequest):
    return await query_draft_status(request)

@router.post('/generate_draft_url',operation_id='generate_draft_url_post')
async def generate_draft_url_route(request: GenerateDraftUrlRequest):
    return await generate_draft_url(request)

@router.post('/query_script',operation_id='query_script_post')
async def query_script_route(request: QueryScriptRequest):
    return await query_script(request) 