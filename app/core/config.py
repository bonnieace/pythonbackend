# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str

    class Config:
        env_file = "../../.env"

settings = Settings()
print('--------------loading---------------------------')
print(settings)

