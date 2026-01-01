from fastapi import APIRouter
from typing import Optional
from api.services.email_service.email_service import EmailService

router = APIRouter(prefix="/api/email", tags=["Email"])

email_service = EmailService()

# ============================================================================================
#  >> Suscribir correo al servicio
# --------------------------------------------------------------------------------------------

@router.post("/subscribe", responses={
    200: {"description": "Usuario suscrito exitosamente para recibir alertas de juegos gratis."},
    500: {"description": "Error interno del servidor."}
})
async def subscribe(email: str):
    return await email_service.subscribe(email)

@router.post("/unsubscribe", responses={
    200: {"description": "Suscripción cancelada exitosamente."},
    500: {"description": "Error interno del servidor."}
})
async def unsubscribe(email: str):
    return await email_service.unsubscribe(email)


@router.post("/send-email", responses={
    200: {"description": "Correo de alerta con las ofertas enviado exitosamente."},
    500: {"description": "Error interno del servidor."}
})
async def send_email(email: str):
    return await email_service.send_email(email)
