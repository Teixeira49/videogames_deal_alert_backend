from api.services.email_service.email_routes import EmailRoutes
from api.core.request_manager.http_client import HttpClient

class EmailService:

    def __init__(self):
        self._client = HttpClient()
        self._route = EmailRoutes()

    async def get_emails(self):
        pass

    async def suscribe_email(self):
        pass

    async def unsubscribe_email(self):
        pass

    async def send_email(self):
        pass