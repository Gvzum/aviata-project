from pydantic import BaseSettings, PostgresDsn, AnyHttpUrl


class Settings(BaseSettings):
    DATABASE_PASSWORD: str = 'aviata_2023'
    DATABASE_USERNAME: str = 'aviata'
    DATABASE_NAME: str = 'aviata'
    DATABASE_HOST: str = 'localhost'
    DATABASE_PORT: int = 5432

    CELERY_BROKER_URL: str

    PROVIDER_A: AnyHttpUrl
    PROVIDER_B: AnyHttpUrl
    NATIONAL_BANK: AnyHttpUrl

    def _format_url(self):
        return '{}:{}@{}:{}/{}'.format(
            self.DATABASE_USERNAME,
            self.DATABASE_PASSWORD,
            self.DATABASE_HOST,
            self.DATABASE_PORT,
            self.DATABASE_NAME,
        )

    @property
    def database_url(self) -> str:
        return f'postgresql://{self._format_url()}'

    @property
    def async_database_url(self) -> str:
        return f'postgresql+asyncpg://{self._format_url()}'

    class Config:
        env_file = './.env'


settings = Settings()
