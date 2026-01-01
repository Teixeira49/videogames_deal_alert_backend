import json
from typing import Optional
from fastapi import HTTPException
#from datetime import datetime

#from api.services.database_service import *
#from api.services.exchanges_service import *
#from api.schemas.book_schema import BookCreate, BookUpdate, LocalCurrency
#from api.models.book import Book
#from api.utils.response_wrapper import *
#from api.utils.constants import Constants
from api.core.wrapper.response_wrapper import api_response
from api.core.request_manager.http_client import HttpClient
from api.services.deals_service.deals_routes import DealsRoutes
from api.services.database_service import DatabaseService

class DealService:

    def __init__(self):
        self._client = HttpClient()
        self._route = DealsRoutes()
        self._db = DatabaseService()

    async def get_deals(self, freeOnly: Optional[bool] = True):
        try:
            #code = await self.api_call.get(url='https://api.isthereanydeal.com/deals/v2/c8a1627742822489318a8a275cbf265973cdc64a') #, headers='c8a1627742822489318a8a275cbf265973cdc64a'
            params = {
                "key": 'c8a1627742822489318a8a275cbf265973cdc64a',
                "shops": "61, 16",  # 61 es el ID de Steam
                "sort": "price", # Las más recientes primero
                "limit": 10      # Traer suficientes para filtrar
            }
            code = await self._client.get(url=self._route.GET_DEALS, params=params)
            if not code:
                raise HTTPException(status_code=404, detail="No se encontraron ofertas.")

            # Verificamos si el último es gratis para traer más páginas si es necesario
            if len(code) == 10:
                code = await self._paginate_if_last_is_free(code, params)

            if freeOnly:
                code = self._filter_free_deals(code)
                # Guardamos en la base de datos los juegos filtrados
                if code.get("list"):
                    self._db.save_free_deals(code["list"])

            return api_response(data=code)
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    async def get_updated_deals(self):
        try:
            #code = await self.api_call.get(url='https://api.isthereanydeal.com/deals/v2/c8a1627742822489318a8a275cbf265973cdc64a') #, headers='c8a1627742822489318a8a275cbf265973cdc64a'
            params = {
                "key": 'c8a1627742822489318a8a275cbf265973cdc64a',
                "shops": "61, 16",  # 61 es el ID de Steam
                "sort": "price", # Las más recientes primero
                "limit": 10      # Traer suficientes para filtrar
            }
            code = await self._client.get(url=self._route.GET_DEALS, params=params)
            if not code:
                raise HTTPException(status_code=404, detail="No se encontraron ofertas.")

            # Verificamos si el último es gratis para traer más páginas si es necesario
            code = await self._paginate_if_last_is_free(code, params)

            return api_response(data=code)
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_db_deals(self):
        """Recupera las ofertas almacenadas en la base de datos local."""
        try:
            deals = self._db.get_all_deals()
            return api_response(data={"list": deals})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def _filter_free_deals(self, data: dict) -> dict:
        """Filtra el JSON original para retornar solo los juegos con precio 0."""
        deals = data.get("list", [])
        # Filtramos buscando precio 0 en los campos comunes de la API ITAD v2
        free_deals = []
        #print('all deals')
        #print(json.dumps(deals, indent=4, sort_keys=True, ensure_ascii=False))
        for deal in deals:
            #print(json.dumps(deal, indent=4, sort_keys=True, ensure_ascii=False))
            if deal.get("deal").get("price").get("amount") == 0:
                free_deals.append(deal)

        #print(len(free_deals))
        
        # Retornamos la misma estructura pero con la lista filtrada
        return {"list": free_deals}
    
    async def _paginate_if_last_is_free(self, data: dict, params: dict) -> dict:
        """
        Verifica si el último juego es gratuito y, de ser así, busca en la siguiente página
        concatenando los resultados de forma recursiva.
        """
        deals = data.get("list", [])
        if not deals:
            return data

        # Comprobamos si el último juego de la lista actual es gratis
        last_deal = deals[-1]
        #print(last_deal)
        is_last_free = (
            last_deal.get('deal').get("price").get("amount") == 0
        )

        next_cursor = data.get("next")
        if is_last_free and next_cursor:
            # Actualizamos el cursor en los parámetros para la siguiente llamada
            params["cursor"] = next_cursor
            next_data = await self._client.get(url='https://api.isthereanydeal.com/deals/v2', params=params)
            if next_data and "list" in next_data:
                data["list"].extend(next_data["list"])
                data["next"] = next_data.get("next")
                # Llamada recursiva por si el último de la nueva página también es gratis
                return await self._paginate_if_last_is_free(data, params)
        
        return data