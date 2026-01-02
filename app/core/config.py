# FILE: app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
	APP_NAME: str = "ResumeAPI"
	APP_ENV: str = "development"
	SECRET_KEY: str
	ALGORITHM: str
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
	REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

	DATABASE_URL: str

	# Email Config
	EMAIL_HOST: str
	EMAIL_PORT: int
	EMAIL_USERNAME: str
	EMAIL_PASSWORD: str

	PROJECT_DOMAIN: str

	GROQ_API_KEY: str

	class Config:
		env_file = ".env"

settings = Settings()
