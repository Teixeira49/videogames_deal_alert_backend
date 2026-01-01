import os

class EmailRoutes:

    BASE_ROUTE = os.getenv("SITE_URL")

    GET_EMAILS = f"{BASE_ROUTE}/view"

    SUSCRIBE_EMAIL = f"{BASE_ROUTE}/subscribe"

    UNSUSCRIBE_EMAIL = f"{BASE_ROUTE}/unsubscribe"

    SEND_EMAIL = f"{BASE_ROUTE}/send"