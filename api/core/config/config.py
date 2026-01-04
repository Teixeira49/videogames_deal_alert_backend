import os 

class Config:

    API_KEY = os.getenv("SITE_KEY")

    CLIENT_ID = os.getenv("SITE_CLIENT_ID")

    BASE_URL = os.getenv("SITE_URL")

    SITE_CLIENT_SECRET = os.getenv("SITE_CLIENT_SECRET")

    SMTP_PORT = 587

    SMTP_SERVER = os.getenv("SMTP_SERVER")

    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    EMAIL_SENDER = os.getenv("EMAIL_SENDER")