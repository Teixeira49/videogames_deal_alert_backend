import os 

class Config:

    API_KEY = os.getenv("SITE_KEY")

    CLIENT_ID = os.getenv("SITE_CLIENT_ID")

    BASE_URL = os.getenv("SITE_URL")

    SITE_CLIENT_SECRET = os.getenv("SITE_CLIENT_SECRET")