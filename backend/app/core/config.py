from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SocialMediaPro"
    environment: str = "dev"
    debug: bool = True

    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/socialmediapro"
    redis_url: str = "redis://redis:6379/0"

    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_exp_minutes: int = 30
    refresh_token_exp_minutes: int = 60 * 24 * 7

    token_encryption_key: str = "0123456789abcdef0123456789abcdef"  # 32 bytes

    razorpay_key_id: str = ""
    razorpay_key_secret: str = ""
    razorpay_webhook_secret: str = ""

    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = ""

    meta_client_id: str = ""
    meta_client_secret: str = ""
    meta_redirect_uri: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
