from fastapi import APIRouter, Depends
from typing import Optional
from api.services.email_service.email_service import EmailService
from api.core.request_manager.http_client import HttpClient
from api.repositories.database_service import DatabaseService
from api.schemas.user import User

router = APIRouter(prefix="/api/email", tags=["Email"])

def get_email_service():
    http_client = HttpClient()
    db_service = DatabaseService()
    return EmailService(http_client, db_service)

# ============================================================================================
#  >> Suscribir correo al servicio
# --------------------------------------------------------------------------------------------

@router.post("/suscribe", responses={
    200: {"description": "Usuario suscrito exitosamente para recibir alertas de juegos gratis."},
    500: {"description": "Error interno del servidor."}
})
async def suscribe(user: User, service: EmailService = Depends(get_email_service)):
    return await service.suscribe_email(user)

@router.post("/unsubscribe", responses={
    200: {"description": "Suscripción cancelada exitosamente."},
    500: {"description": "Error interno del servidor."}
})
async def unsubscribe(userId: int, service: EmailService = Depends(get_email_service)):
    return await service.unsuscribe_email(userId)


@router.post("/send-email", responses={
    200: {"description": "Correo de alerta con las ofertas enviado exitosamente."},
    500: {"description": "Error interno del servidor."}
})
async def send_email(service: EmailService = Depends(get_email_service),):
    return await service.send_email()