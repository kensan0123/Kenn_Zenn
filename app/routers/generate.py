from dataclasses import dataclass
from fastapi import APIRouter
from pydantic import BaseModel
from app.services.generate_service import GenerateService

router = APIRouter()

class GenerateRequest(BaseModel):
    title: str
    emoji: str
    content: str
    slug: str | None = None

generate_service = GenerateService()

@router.post("/")
def generate_article_api(req: GenerateRequest):
    generated_article_slug: str = generate_service.generate_article(
        title=req.title,
        emoji=req.emoji,
        content=req.content,
        slug=req.slug,
    )
    
    generated_added_topic_article_slug: str = generate_service.add_topics(article_slug=generated_article_slug, topic="Python")
    
    return {
        "status": "generated!",
        "slug": generated_added_topic_article_slug,
    }
