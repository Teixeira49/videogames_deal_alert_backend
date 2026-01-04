from fastapi import APIRouter, Depends, BackgroundTasks
from typing import Optional
from api.services.email_service.email_service import EmailService
from api.core.request_manager.http_client import HttpClient
from api.repositories.database_service import DatabaseService
from api.core.wrapper.response_wrapper import api_response
from api.schemas.user import User

router = APIRouter(prefix="/api/email", tags=["Email"])

def get_email_service():
    http_client = HttpClient()
    db_service = DatabaseService()
    return EmailService(http_client, db_service)

# ============================================================================================
#  >> Suscribir correo al servicio
# --------------------------------------------------------------------------------------------

@router.post("/subscribe", responses={
    200: {"description": "Usuario suscrito exitosamente para recibir alertas de juegos gratis."},
    500: {"description": "Error interno del servidor."}
})
async def subscribe(user: User, service: EmailService = Depends(get_email_service)):
    return await service.subscribe_email(user)

@router.post("/disable", responses={
    200: {"description": "Suscripción cancelada exitosamente."},
    500: {"description": "Error interno del servidor."}
})
async def disable_subscription(userId: int, service: EmailService = Depends(get_email_service)):
    return await service.disable_subscription(userId)

@router.post("/enable",  responses={
    200: {"description": "Suscripción habilitada exitosamente."},
    500: {"description": "Error interno del servidor."}
})
async def enable_subscription(userId: int, service: EmailService = Depends(get_email_service)):
    return await service.enable_subscription(userId)

@router.post("/send-email-to", responses={
    200: {"description": "Correo de alerta con las ofertas enviado exitosamente."},
    500: {"description": "Error interno del servidor."}
})
async def send_email_to(email: str, service: EmailService = Depends(get_email_service)):
    return await service.send_individual_email(email)

@router.post("/send-email", responses={
    200: {"description": "Correo de alerta con las ofertas enviado exitosamente."},
    500: {"description": "Error interno del servidor."}
})
async def send_email(service: EmailService = Depends(get_email_service),):
    BackgroundTasks.add_task(service.send_email)
    return api_response(message="Correos en proceso de envio exitoso")