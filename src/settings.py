from pydantic import BaseSettings


class Settings(BaseSettings):
    pg_database: str = "database"
    pg_user: str = "postgres"
    pg_password: str = "postgres"
    pg_host: str = "localhost"
    pg_port: int = 5432

    redis_host: str = "localhost"
    redis_port: int = 6379

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
