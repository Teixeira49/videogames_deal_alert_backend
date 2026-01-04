from api.services.email_service.email_routes import EmailRoutes
from api.core.request_manager.http_client import HttpClient
from api.core.config.config import Config as conf
from api.core.errors.base_exceptions import DatabaseError
from api.schemas.user import User
from api.repositories.database_service import DatabaseService
from api.core.wrapper.response_wrapper import api_response
from api.utils.html.game_html import create_deals_email_body

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailService:

    def __init__(self, http_client: HttpClient, db_service: DatabaseService):
        self._client = http_client
        self._route = EmailRoutes()
        self._db = db_service

    async def get_emails(self):
        pass

    async def subscribe_email(self, user: User):
        """Registra un nuevo usuario en la base de datos para suscripción."""
        try:
            register = self._db.add_user(user)
            if register != None:
                return api_response(message="Correo registrado exitosamente")
            return api_response(message="Correo ya registrado", status_code=422, detail='ERROR')
        except Exception as e:
            raise DatabaseError(f"Error al registrar en base de datos: {str(e)}")

    async def disable_subscription(self, userId):
        try:
            disable = self._db.disable_user(user_id=userId)
            if disable == True:
                return api_response(message="Correo desabilitado exitosamente")
            return api_response(message="Error desabilitando usuario", status_code=400, detail='ERROR')
        except Exception as e:
            raise DatabaseError(f"Error al registrar en base de datos: {str(e)}")


    async def enable_subscription(self, userId):
        try:
            enable = self._db.enable_user(user_id=userId)
            if enable == True:
                return api_response(message="Correo habilitado exitosamente")
            return api_response(message="Error habilitando usuario", status_code=400, detail='ERROR')
        except Exception as e:
            raise DatabaseError(f"Error al registrar en base de datos: {str(e)}")

    async def send_email(self):
        users = self._db.get_active_users()
        deals = self._db.get_all_deals()

        body = create_deals_email_body(deals)
        
        for i in users:
            self.send_email_for_user(i, 'Nuevos juegos gratuitos por tiempo limitado', body)

    async def send_individual_email(self, target):
        deals = self._db.get_all_deals()
        body = create_deals_email_body(deals)
        return self.send_email_for_user(target, 'Nuevos juegos gratuitos por tiempo limitado', body)
        
    def send_email_for_user(self, target, subject, body_msg):
        """Envía un solo correo usando SMTP"""
        try:
            msg = MIMEMultipart()
            msg['From'] = conf.EMAIL_SENDER
            msg['To'] = target
            msg['Subject'] = subject

            msg.attach(MIMEText(body_msg, 'html'))

            print(body_msg)

            server = smtplib.SMTP(conf.SMTP_SERVER, conf.SMTP_PORT)
            server.starttls() # Encriptar conexión
            server.login(conf.EMAIL_SENDER, conf.EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            print(f"✅ Enviado a: {target}")
            return api_response(message=f"✅ Enviado a: {target}")
        except Exception as e:
            print(f"❌ Error enviando a {target}: {e}")
            return api_response(message=f"❌ Error enviando a {target}: {e}", status_code=400, detail='ERROR')
