from fastapi import APIRouter, Depends
from typing import Optional
from api.services.deals_service.deals_service import DealService
from api.core.request_manager.http_client import HttpClient
from api.repositories.database_service import DatabaseService

router = APIRouter(prefix="/api/deals", tags=["Deals"])

def get_deals_service():
    # Aquí inyectamos las dependencias manualmente o mediante un contenedor
    http_client = HttpClient()
    db_service = DatabaseService()
    return DealService(http_client, db_service)

# ============================================================================================
#  >> Obtener ofertas guardadas en Base de Datos
# --------------------------------------------------------------------------------------------

@router.get("/view", responses={
    200: {"description": "Lista de ofertas en DB recuperada exitosamente."},
    500: {"description": "Error interno del servidor."}
})
async def get_db_deals(service: DealService = Depends(get_deals_service)):
    return await service.get_db_deals()

# ============================================================================================
#  >> Obtener todas las ofertas gratuitas
# --------------------------------------------------------------------------------------------

@router.get("/view/external", responses={
    200: {"description": "Lista de ofertas de videojuegos obtenida exitosamente."},
    404: {"description": "No se encontraron ofertas disponibles."},
    500: {"description": "Error interno del servidor."}
})
async def get_deals(
    freeOnly: Optional[bool] = True, 
    service: DealService = Depends(get_deals_service)
):
    return await service.get_deals(freeOnly)

# ============================================================================================
#  >> Obtener y enviar oferta mas reciente
# --------------------------------------------------------------------------------------------
@router.post("/update", responses={
    200: {"description": "Ofertas actualizadas y procesadas exitosamente."},
    404: {"description": "No se encontraron ofertas nuevas para procesar."},
    500: {"description": "Error interno del servidor."}
})
async def update_deals(service: DealService = Depends(get_deals_service)):
    return await service.get_updated_deals()