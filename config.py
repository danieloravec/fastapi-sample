from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 15
    tatum_api_url: str
    tatum_api_key: str
    txs_period_days: int = 90

    class Config:
        env_file = ".env"


settings = Settings()
