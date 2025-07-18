from app.routes.video_routes import router as video_router
from app.routes.audio_routes import router as audio_router
from app.routes.text_routes import router as text_router
from app.routes.image_routes import router as image_router
from app.routes.effect_routes import router as effect_router
from app.routes.draft_routes import router as draft_router
from app.routes.meta_routes import router as meta_router

__all__ = [
    'video_router',
    'audio_router',
    'text_router',
    'image_router',
    'effect_router',
    'draft_router',
    'meta_router'
] 