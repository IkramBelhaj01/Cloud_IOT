import os

class Config:
    SECRET_KEY = "supersecretkey"
    DATABASE_URL = "postgresql://admin:1234@db/db_ms"
    REDIS_URL = "redis://cache:6379/0"  # Assurez-vous que le nom du service Redis est bien 'cache' dans Docker
