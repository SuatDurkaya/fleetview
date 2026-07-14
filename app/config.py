from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    hetzner_api_token: str = ""
    digitalocean_api_token: str = ""
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "eu-central-1"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()