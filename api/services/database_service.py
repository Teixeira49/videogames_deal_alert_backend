import sqlite3
import json
from typing import List, Dict

class DatabaseService:
    def __init__(self, db_name="deals.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        """Inicializa la tabla si no existe."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS free_deals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ext_id TEXT UNIQUE,
                title TEXT UNIQUE,
                shop TEXT,
                is_mature BOOLEAN,
                store_link TEXT,
                image_url TEXT,
                original_price REAL,
                publish_date TEXT,
                expiry_date TEXT,
                platforms TEXT,
                is_deleted BOOLEAN DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    def save_free_deals(self, deals: List[Dict]):
        """Guarda una lista de ofertas ignorando las que ya existen por título."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        for deal in deals:
            # Mapeo de campos desde el JSON de ITAD v2
            ext_id = deal.get("id")
            title = deal.get("title")
            shop = deal.get('deal').get("shop", {}).get("name") if isinstance(deal.get("shop"), dict) else "N/A"
            is_mature = deal.get("mature", False)
            store_link = deal.get('deal').get("url")
            image_url = deal.get("assets").get("boxart")
            original_price = deal.get("deal").get("regular").get("amount") if isinstance(deal, dict) else 0
            publish_date = deal.get("deal").get("timestamp")
            expiry_date = deal.get("deal").get("expiry")
            platforms = json.dumps(deal.get("platforms", [])) # Guardamos la lista como string JSON

            cursor.execute('''
                INSERT OR IGNORE INTO free_deals 
                (ext_id, title, shop, is_mature, store_link, image_url, original_price, publish_date, expiry_date, platforms)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (ext_id, title, shop, is_mature, store_link, image_url, original_price, publish_date, expiry_date, platforms))
        
        conn.commit()
        conn.close()

    def get_all_deals(self) -> List[Dict]:
        """Obtiene todos los deals almacenados que no estén marcados como eliminados."""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM free_deals WHERE is_deleted = 0')
        rows = cursor.fetchall()
        conn.close()
        
        deals = []
        for row in rows:
            deal = dict(row)
            # Convertimos el string JSON de plataformas de vuelta a una lista
            if deal.get("platforms"):
                deal["platforms"] = json.loads(deal["platforms"])
            deals.append(deal)
        return deals