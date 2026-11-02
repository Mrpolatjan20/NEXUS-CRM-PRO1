from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NEXUS CRM API"
    database_url: str = "sqlite:///./nexus_crm.db"
    secret_key: str = "nexus_secret_key_change_later"
    access_token_expire_minutes: int = 720
    cors_origins: str = "*"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    @property
    def allowed_origins(self) -> list[str]:
        return [
            item.strip()
            for item in self.cors_origins.split(",")
            if item.strip()
        ]


settings = Settings()