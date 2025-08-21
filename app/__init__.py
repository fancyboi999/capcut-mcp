from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_mcp import FastApiMCP
from app.routes import (
    video_router,
    audio_router,
    text_router,
    image_router,
    effect_router,
    draft_router,
    meta_router
)
from settings.local import PORT

def create_app() -> FastAPI:
    app = FastAPI(
        title="CapCut API",
        description="CapCut API for video editing",
        version="1.0.0"
    )

    # 配置 CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许所有来源
        allow_credentials=True,
        allow_methods=["*"],  # 允许所有方法
        allow_headers=["*"],  # 允许所有头部
    )
    
    # 注册路由
    app.include_router(video_router)
    app.include_router(audio_router)
    app.include_router(text_router)
    app.include_router(image_router)
    app.include_router(effect_router)
    app.include_router(draft_router)
    app.include_router(meta_router)
    
    # 挂载 MCP
    mcp = FastApiMCP(app)
    mcp.mount()
    
    return app 