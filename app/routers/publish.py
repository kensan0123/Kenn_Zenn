from dataclasses import dataclass
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.publish_service import PublishService, PublishResult
from typing import Literal

router = APIRouter()
publish_service = PublishService()

class PublishRequest(BaseModel):
    slug: str

class PublishResponse(BaseModel):
    status: Literal["published!", "failed"]
    slug: str

@router.post("/")
def publish_article_api(req: PublishRequest) -> PublishResponse:
    result: PublishResult = publish_service.publish_article(req.slug)
    if result.result:
        publish_response: PublishResponse = PublishResponse(status="published!", slug=req.slug)

        return publish_response
    else:
        publish_response: PublishResponse = PublishResponse(status="failed", slug=req.slug)

        return publish_response
