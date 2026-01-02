# FILE: app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):

	DATABASE_URL: str

	CLERK_SECRET_KEY: str
	CLERK_ISSUER: str
	CLERK_JWKS_URL: str

	GROQ_API_KEY: str

	class Config:
		env_file = ".env"

settings = Settings()
