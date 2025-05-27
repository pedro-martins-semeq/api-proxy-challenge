from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    external_api_url: str = "https://internal-stream.semeq.com/api"


settings = Settings()
