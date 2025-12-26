from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Our domain errors that the service raises
from app.domain.errors import DocumentNotFoundError, InvalidDocumentStateError, InvalidDocumentInputError

from app.api.routes.documents import router as documents_router
app = FastAPI(title="Document Processing API")

# Global handler for when document doesn't exist
@app.exception_handler(DocumentNotFoundError)
async def not_found_handler(request: Request, exc: DocumentNotFoundError) -> JSONResponse:
    # Always return 404 with a clean message
    return JSONResponse(
        status_code=404,
        content={"detail":"Document not found"}
    )

# Global handler for invalid status transitions
@app.exception_handler(InvalidDocumentStateError)
async def invalid_state_handler(request: Request, exc: InvalidDocumentStateError) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={"detail":str(exc)},
    )

@app.exception_handler(InvalidDocumentInputError)
async def invalid_input_handler(request: Request, exc: InvalidDocumentInputError) -> JSONResponse:
    # 422 = Unprocessable Entity - standard for validation/input errors
    return JSONResponse(
        status_code=422,
        content={"detail":str(exc)},
    )


app.include_router(documents_router)