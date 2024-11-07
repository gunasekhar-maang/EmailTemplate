import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    FROM_EMAIL = os.getenv("FROM_EMAIL")
