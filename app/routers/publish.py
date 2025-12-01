from dataclasses import dataclass
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.publish_service import PublishService, PublishResult

router = APIRouter()
publish_service = PublishService()

class PublishRequest(BaseModel):
    slug: str

@router.post("/")
def publish_article_api(req: PublishRequest):
    result: PublishResult = publish_service.publish_article(req.slug)
    if result.result:
        return {
            "status": "published!",
            "slug": req.slug,
        }
    else:
        return False
