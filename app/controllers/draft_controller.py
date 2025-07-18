from fastapi.responses import JSONResponse
from app.schemas import (
    CreateDraftRequest, 
    SaveDraftRequest, 
    QueryDraftStatusRequest, 
    GenerateDraftUrlRequest,
    QueryScriptRequest,
    ResponseModel
)
from create_draft import create_draft as create_draft_impl
from save_draft_impl import save_draft_impl, query_task_status, query_script_impl
from util import generate_draft_url as utilgenerate_draft_url
from settings.local import DRAFT_DOMAIN, PREVIEW_ROUTER

async def create_draft_service(request: CreateDraftRequest) -> JSONResponse:
    result = ResponseModel()
    
    try:
        # Create new draft
        script, draft_id = create_draft_impl(width=request.width, height=request.height)
        
        result.success = True
        result.output = {
            "draft_id": draft_id,
            "draft_url": utilgenerate_draft_url(draft_id)
        }
        return JSONResponse(content=result.dict())
        
    except Exception as e:
        result.error = f"Error occurred while creating draft: {str(e)}."
        return JSONResponse(content=result.dict())

async def save_draft(request: SaveDraftRequest) -> JSONResponse:
    result = ResponseModel()
    
    # Validate required parameters
    if not request.draft_id:
        result.error = "Hi, the required parameter 'draft_id' is missing. Please add it and try again."
        return JSONResponse(content=result.dict())
    
    try:
        # Call save_draft_impl method, start background task
        draft_result = save_draft_impl(request.draft_id, request.draft_folder)
        
        result.success = True
        result.output = draft_result
        return JSONResponse(content=result.dict())
        
    except Exception as e:
        result.error = f"Error occurred while saving draft: {str(e)}."
        return JSONResponse(content=result.dict())

async def query_draft_status(request: QueryDraftStatusRequest) -> JSONResponse:
    result = ResponseModel()
    
    # Validate required parameters
    if not request.task_id:
        result.error = "Hi, the required parameter 'task_id' is missing. Please add it and try again."
        return JSONResponse(content=result.dict())
    
    try:
        # Get task status
        task_status = query_task_status(request.task_id)
        
        if task_status["status"] == "not_found":
            result.error = f"Task with ID {request.task_id} not found. Please check if the task ID is correct."
            return JSONResponse(content=result.dict())
        
        result.success = True
        result.output = task_status
        return JSONResponse(content=result.dict())
        
    except Exception as e:
        result.error = f"Error occurred while querying task status: {str(e)}."
        return JSONResponse(content=result.dict())

async def generate_draft_url(request: GenerateDraftUrlRequest) -> JSONResponse:
    result = ResponseModel()
    
    # Validate required parameters
    if not request.draft_id:
        result.error = "Hi, the required parameter 'draft_id' is missing. Please add it and try again."
        return JSONResponse(content=result.dict())
    
    try:
        draft_result = { "draft_url": f"{DRAFT_DOMAIN}{PREVIEW_ROUTER}?={request.draft_id}" }
        
        result.success = True
        result.output = draft_result
        return JSONResponse(content=result.dict())
        
    except Exception as e:
        result.error = f"Error occurred while generating draft URL: {str(e)}."
        return JSONResponse(content=result.dict())

async def query_script(request: QueryScriptRequest) -> JSONResponse:
    result = ResponseModel()

    # Validate required parameters
    if not request.draft_id:
        result.error = "Hi, the required parameter 'draft_id' is missing. Please add it and try again."
        return JSONResponse(content=result.dict())

    try:
        # Call query_script_impl method
        script = query_script_impl(draft_id=request.draft_id, force_update=request.force_update)
        
        if script is None:
            result.error = f"Draft {request.draft_id} does not exist in cache."
            return JSONResponse(content=result.dict())
        
        # Convert script object to JSON serializable dictionary
        script_str = script.dumps()
        
        result.success = True
        result.output = script_str
        return JSONResponse(content=result.dict())

    except Exception as e:
        result.error = f"Error occurred while querying script: {str(e)}."
        return JSONResponse(content=result.dict()) 