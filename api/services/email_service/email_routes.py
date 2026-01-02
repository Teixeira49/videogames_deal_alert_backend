from api.core.config.config import Config as conf

class EmailRoutes:

    BASE_ROUTE = conf.BASE_URL

    #GET_EMAILS = f"{BASE_ROUTE}/view"

    SUSCRIBE_EMAIL = f"{BASE_ROUTE}/subscribe"

    UNSUSCRIBE_EMAIL = f"{BASE_ROUTE}/unsubscribe"

    SEND_EMAIL = f"{BASE_ROUTE}/send"