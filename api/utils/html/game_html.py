from datetime import datetime
from typing import List

def create_single_deal_html(deal: dict) -> str:
    """Genera el cuerpo HTML para una sola oferta basado en el diccionario de datos."""
    
    title = deal.get("title", "Título Desconocido")
    image_url = deal.get("image_url", "")
    store_link = deal.get("store_link", "#")
    is_mature = deal.get("is_mature", 0)
    original_price = deal.get("original_price", 0)
    shop = deal.get("shop", "Tienda")
    platforms = deal.get("platforms", [])
    
    # Formateo de fechas (ISO 8601 a formato legible)
    def format_date(date_str):
        if not date_str:
            return "Fecha no disponible"
        try:
            # Parsea la fecha (ej: 2025-12-22T19:18:23+01:00)
            dt = datetime.fromisoformat(date_str)
            return dt.strftime("%d/%m/%Y %H:%M")
        except ValueError:
            return date_str

    publish_date = format_date(deal.get("publish_date"))
    expiry_date = format_date(deal.get("expiry_date"))

    # Etiqueta R-18 condicional
    mature_badge = ""
    if is_mature:
        mature_badge = '<span style="background-color: #dc3545; color: white; padding: 2px 6px; border-radius: 4px; font-size: 12px; margin-left: 5px; vertical-align: middle;">R-18</span>'

    # Lista de plataformas como string
    platforms_str = ", ".join(platforms) if platforms else "PC"

    return f"""
    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin-bottom: 20px; font-family: Arial, sans-serif; max-width: 600px; background-color: #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
        <div style="text-align: center; margin-bottom: 15px;">
            <img src="{image_url}" alt="Portada de {title}" style="max-width: 100%; height: auto; border-radius: 4px;">
        </div>
        <h2 style="color: #333; margin-top: 0; font-size: 20px;">{title}{mature_badge}</h2>
        <p style="color: #555; font-size: 14px; margin: 5px 0;"><strong>Tienda:</strong> {shop}</p>
        <p style="color: #555; font-size: 14px; margin: 5px 0;"><strong>Plataformas:</strong> {platforms_str}</p>
        <p style="color: #555; font-size: 14px; margin: 5px 0;">
            <strong>Precio:</strong> <span style="text-decoration: line-through;">${original_price}</span> <span style="color: #28a745; font-weight: bold;">GRATIS</span>
        </p>
        <p style="color: #777; font-size: 13px; margin: 10px 0;">
            Disponible desde el {publish_date} hasta el {expiry_date}
        </p>
        <a href="{store_link}" target="_blank" style="display: inline-block; background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 10px;">Ir a la Oferta</a>
    </div>
    """

def create_deals_email_body(deals: List[dict]) -> str:
    """Genera el cuerpo completo del correo iterando sobre la lista de ofertas."""
    
    deals_html = ""
    if not deals:
        deals_html = '<p style="text-align: center; color: #555;">No hay ofertas activas en este momento.</p>'
    else:
        for deal in deals:
            deals_html += create_single_deal_html(deal)

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Alertas de Juegos Gratis</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #f4f4f4; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff;">
            <div style="background-color: #0d6efd; padding: 20px; text-align: center;">
                <h1 style="color: #ffffff; margin: 0; font-size: 24px;">Videogames Deal Alert</h1>
            </div>
            <div style="padding: 20px;">
                <p style="color: #333; text-align: center; margin-bottom: 25px;">¡Hola! Aquí tienes las últimas ofertas de juegos gratuitos que hemos encontrado para ti.</p>
                <div style="display: flex; flex-direction: column; align-items: center;">
                    {deals_html}
                </div>
            </div>
            <div style="background-color: #f8f9fa; padding: 15px; text-align: center; border-top: 1px solid #eee;">
                <p style="color: #6c757d; font-size: 12px; margin: 0;">Estás recibiendo este correo porque te suscribiste a nuestras alertas.</p>
            </div>
        </div>
    </body>
    </html>
    """