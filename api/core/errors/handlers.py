from fastapi import Request
from fastapi.responses import JSONResponse
from api.core.errors.base_exceptions import BaseAppException

async def app_exception_handler(request: Request, exc: BaseAppException):
    """Captura excepciones personalizadas y devuelve un formato JSON estándar."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.message
        },
    )