# 🎮 Free Games Tracker (FastAPI)

Este proyecto es un servicio automatizado construido con FastAPI que monitorea las tiendas de Steam y Epic Games en busca de juegos que estén 100% gratis por tiempo limitado. Utiliza la API de IsThereAnyDeal para obtener datos precisos y envía notificaciones por correo electrónico con el enlace directo para reclamar la oferta.

## ✨ Características Actuales

* Monitoreo Automático: Consulta la API de IsThereAnyDeal (v2) para detectar juegos con un 100% de descuento.
* Soporte Multitienda: Filtrado específico para Steam y Epic Games Store.
* Persistencia de Datos: Uso de SQLite3 para registrar las ofertas ya notificadas y evitar correos duplicados.
* Notificaciones por Email: Envío de alertas automáticas que incluyen el título del juego, la tienda y el enlace directo a la oferta.
* Arquitectura Moderna: Basado en FastAPI para una ejecución asíncrona y eficiente.
---
## 🛠️ Requisitos de Ejecución
Antes de comenzar, asegúrate de tener instalado:

- Python 3.9+ 🐍
- SQLite3 (viene incluido por defecto con Python) 💾
- Una API Key de IsThereAnyDeal 👾

## 🚀 Instalación y Configuración
Sigue estos pasos para levantar el proyecto en tu entorno local:

1. Clonar el repositorio
```
git clone https://github.com/tu-usuario/nombre-del-repo.git
cd nombre-del-repo
```

2. Crear y activar un entorno virtual
```
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Instalar dependencias

El proyecto utiliza FastAPI, Uvicorn (servidor), y HTTPX (para peticiones asíncronas).
```
pip install fastapi uvicorn httpx pydantic-settings
```

4. Variables de Entorno

Crea un archivo .env en la raíz del proyecto y añade tus credenciales

Nota: Recuerda para esta parte solicitar a la api de IsThereAnyDeal tu clave secreta (link: https://docs.isthereanydeal.com)

---
⚡️ Ejecutar proyecto

```
uvicorn main:app --reload
```
