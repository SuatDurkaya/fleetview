from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    hetzner_api_token: str = ""
    digitalocean_api_token: str = ""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = ""
    api_secret_key: str = ""
    admin_username: str = ""
    admin_password_hash: str = ""
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    prometheus_url: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()