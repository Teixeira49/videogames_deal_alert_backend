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
                type TEXT,
                is_deleted BOOLEAN DEFAULT 0
            )
        ''')

        # Verificación de migración: Agregar columna 'type' si no existe
        cursor.execute("PRAGMA table_info(free_deals)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'type' not in columns:
            cursor.execute('ALTER TABLE free_deals ADD COLUMN type TEXT')

        conn.commit()
        conn.close()

    def save_free_deals(self, deals: List[Dict]):
        """Guarda una lista de ofertas ignorando las que ya existen por título."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # 1. Obtener los IDs externos de la lista actual de la API
        current_api_ids = [str(deal.get("id")) for deal in deals if deal.get("id")]

        # 2. Marcar como eliminados los que están en DB pero ya no vienen en la API
        if current_api_ids:
            placeholders = ', '.join(['?'] * len(current_api_ids))
            query = f'UPDATE free_deals SET is_deleted = 1 WHERE is_deleted = 0 AND ext_id NOT IN ({placeholders})'
            cursor.execute(query, current_api_ids)
        else:
            # Si la lista de la API está vacía, todos los juegos activos pasan a is_deleted = 1
            cursor.execute('UPDATE free_deals SET is_deleted = 1 WHERE is_deleted = 0')

        # 3. Insertar nuevos o actualizar existentes (Upsert)
        for deal in deals:
            deal_info = deal.get('deal', {})
            ext_id = deal.get("id")
            title = deal.get("title")
            deal_type = deal.get("type", "game")  # 'game' o 'dlc'
            shop = deal_info.get("shop", {}).get("name", "N/A")
            is_mature = deal.get("mature", False)
            store_link = deal_info.get("url")
            image_url = deal.get("assets", {}).get("boxart")
            original_price = deal_info.get("regular", {}).get("amount", 0)
            publish_date = deal_info.get("timestamp")
            expiry_date = deal_info.get("expiry")
            platforms = json.dumps(deal.get("platforms", ['Windows', 'Mac', 'Linux'])) # Guardamos la lista como string JSON

            cursor.execute('''
                INSERT INTO free_deals 
                (ext_id, title, shop, is_mature, store_link, image_url, original_price, publish_date, expiry_date, platforms, type, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                ON CONFLICT(ext_id) DO UPDATE SET
                    is_deleted = 0,
                    title = excluded.title,
                    shop = excluded.shop,
                    type = excluded.type,
                    is_mature = excluded.is_mature,
                    store_link = excluded.store_link,
                    image_url = excluded.image_url,
                    expiry_date = excluded.expiry_date,
                    original_price = excluded.original_price,
                    platforms = excluded.platforms
            ''', (ext_id, title, shop, is_mature, store_link, image_url, original_price, publish_date, expiry_date, platforms, deal_type))

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