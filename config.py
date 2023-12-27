from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # database
    database_hostname: str
    datebase_port: str
    database_name: str
    database_username: str
    database_password: str
    
    # JWT
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings = Settings()