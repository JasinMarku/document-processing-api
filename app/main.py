from fastapi import FastAPI

from app.api.routes.documents import router as documents_router

app = FastAPI(title="Document Processing API")

app.include_router(documents_router)