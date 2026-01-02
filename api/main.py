from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from api.utils.html.root_html import root_html
import traceback
from dotenv import load_dotenv

load_dotenv()

try:
    from api.routes.deals_controller import router as deals_controller
    from api.routes.email_controller import router as email_controller

    app = FastAPI(title="videogames-deals-api")
    app.include_router(deals_controller)
    app.include_router(email_controller)

    @app.get("/", response_class=HTMLResponse, tags=["Root"])
    def root():
        html_content = root_html()
        return HTMLResponse(content=html_content, status_code=200)

except Exception as e:
    tb = traceback.format_exc()
    app = FastAPI(title="videogames-deals-api - Import Error")
    exception = Exception.with_traceback

    @app.get("/")
    async def root():
        return {"error": "import_failed", "message": str(exception)}

    @app.get("/__import_error")
    async def import_error():
        # endpoint temporal para ver la traza completa en los logs/response
        return {"traceback": tb}