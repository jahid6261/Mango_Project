from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine


class Settings(BaseSettings):

    DATABASE_URL: str
    SECRET_KEY: str

    ADMIN_EMAIL: str

    ADMIN_PASSWORD: str

    BASE_URL: str
    
    """
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str
    """
    
   
    RESEND_API_KEY: str
    EMAIL_FROM: str

    # Cloudinary settings
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str


    model_config = SettingsConfigDict(
        env_file=".env",
        extra='ignore'
    )


settings = Settings()

engine = create_async_engine(settings.DATABASE_URL)