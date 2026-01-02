from api.services.email_service.email_routes import EmailRoutes
from api.core.request_manager.http_client import HttpClient
from api.core.errors.base_exceptions import ExternalAPIError, DatabaseError
from api.schemas.user import User
from api.repositories.database_service import DatabaseService
from api.core.wrapper.response_wrapper import api_response

class EmailService:

    def __init__(self, http_client: HttpClient, db_service: DatabaseService):
        self._client = http_client
        self._route = EmailRoutes()
        self._db = db_service

    async def get_emails(self):
        pass

    async def suscribe_email(self, user: User):
        """Registra un nuevo usuario en la base de datos para suscripción."""
        try:
            register = self._db.add_user(user)
            if register != None:
                return api_response(message="Correo registrado exitosamente")
            return api_response(message="Correo ya registrado", status_code=422, detail='ERROR')
        except Exception as e:
            raise DatabaseError(f"Error al registrar en base de datos: {str(e)}")

    async def unsuscribe_email(self):
        pass

    async def send_email(self):
        pass