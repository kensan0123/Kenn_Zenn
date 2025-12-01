from fastapi import APIRouter
from pydantic import BaseModel
from app.services.file_service import FileService

router = APIRouter()
file_service = FileService()

class UploadRequest(BaseModel):
    slug: str
    content: str

@router.post("/")
def upload_markdown(req: UploadRequest):
    file_path = file_service.save_markdown(req.slug, req.content)
    return {
        "status": "stored",
        "path": file_path,
    }
