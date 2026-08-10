from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    debug: bool = False
    mcp_resource_url: str
    scalekit_authorization_server: str
    mcp_resource_metadata_url: str
    scalekit_environment_url: str
    scalekit_client_id: str
    scalekit_client_secret: str
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()  # type: ignore
