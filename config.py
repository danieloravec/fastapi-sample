from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 15

    class Config:
        env_file = ".env"


settings = Settings()
