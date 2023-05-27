from pydantic import BaseSettings

class Settings(BaseSettings):
    db_name: str
    db_port: str
    db_username: str
    db_password: str
    db_host: str
    token_expiry_time: int
    jwt_key: str
    algorithm: str

    class Config:
        env_file = ".env"

settings = Settings()

