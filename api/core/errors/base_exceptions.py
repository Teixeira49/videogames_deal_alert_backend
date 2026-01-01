class BaseAppException(Exception):
    """Base para todas las excepciones de la aplicación."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ExternalAPIError(BaseAppException):
    """Error al comunicarse con IsThereAnyDeal u otros servicios externos."""
    def __init__(self, message: str = "Error al obtener datos del proveedor externo"):
        super().__init__(message, status_code=502)

class DatabaseError(BaseAppException):
    """Error en operaciones de base de datos."""
    def __init__(self, message: str = "Error en la persistencia de datos"):
        super().__init__(message, status_code=500)