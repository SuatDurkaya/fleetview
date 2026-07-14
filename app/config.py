from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    hetzner_api_token: str = ""
    digitalocean_api_token: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()