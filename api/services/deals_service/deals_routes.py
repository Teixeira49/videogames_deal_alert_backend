import os
from api.core.config.config import Config as conf

class DealsRoutes:

    BASE_ROUTE = conf.BASE_URL

    GET_DEALS = f"{BASE_ROUTE}/deals/v2"