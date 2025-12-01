from fastapi import FastAPI
from app.routers.generate import router as generate_router
from app.routers.upload import router as upload_router
from app.routers.publish import router as publish_router

app = FastAPI(
    title="Kenn Zenn Publishing Service",
    version="0.1.0",
)

@app.get("/")
def health_check():
    return {"status": "running", "service": "Kenn_Zenn"}

app.include_router(generate_router, prefix="/generate", tags=["generate"])
app.include_router(upload_router, prefix="/upload", tags=["upload"])
app.include_router(publish_router, prefix="/publish", tags=["publish"])
