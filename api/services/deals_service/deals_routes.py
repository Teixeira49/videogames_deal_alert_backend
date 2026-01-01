import os

class DealsRoutes:

    BASE_ROUTE = os.getenv("SITE_URL")

    GET_DEALS = f"{BASE_ROUTE}/deals/v2"