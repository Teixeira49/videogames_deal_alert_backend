from fastapi import APIRouter
from typing import Optional
from api.services.deals_service.deals_service import DealService

router = APIRouter(prefix="/api/deals", tags=["Deals"])

deals_service = DealService()

# ============================================================================================
#  >> Obtener todas las ofertas gratuitas
# --------------------------------------------------------------------------------------------

@router.get("/view-deals", responses={
    200: {"description": "Lista de libros encontrada exitosamente."},
    404: {"description": "No se encontraron libros."},
    500: {"description": "Error interno del servidor."}
})
async def get_deals(freeOnly: Optional[bool] = True):
    return await deals_service.get_deals(freeOnly)

# ============================================================================================
#  >> Obtener ofertas guardadas en Base de Datos
# --------------------------------------------------------------------------------------------

@router.get("/db-deals", responses={
    200: {"description": "Lista de ofertas en DB recuperada exitosamente."},
    500: {"description": "Error interno del servidor."}
})
async def get_db_deals():
    return await deals_service.get_db_deals()

# ============================================================================================
#  >> Obtener y enviar oferta mas reciente
# --------------------------------------------------------------------------------------------
@router.post("/update-deals", responses={
    200: {"description": "Lista de libros encontrada exitosamente."},
    404: {"description": "No se encontraron libros."},
    500: {"description": "Error interno del servidor."}
})
async def update_deals():
    return await deals_service.get_updated_deals()
"""

# ============================================================================================
#  >> Suscribir correo al servicio
# --------------------------------------------------------------------------------------------

@router.get("/books/all", responses={
    200: {"description": "Lista de libros encontrada exitosamente."},
    404: {"description": "No se encontraron libros."},
    500: {"description": "Error interno del servidor."}
})
async def get_books():
    return await deals_service.get_books()
    """