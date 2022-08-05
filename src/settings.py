from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    redis_host: str = Field(env='REDIS_HOST')
    redis_port: int = Field(env='REDIS_PORT')
    app_secret: str = Field(env='APP_SECRET')
    refresh_ttl: int = Field(env='REFRESH_TOKEN_TTL_MINS')
    access_ttl: int = Field(env='ACCESS_TOKEN_TTL_MINS')
    invalid_tokens_ttl: int = Field(env='INVALID_TOKENS_TTL')

    class Config:
        env_file = 'config/.env.app'


class DBSettings(BaseSettings):
    ps_user: str = Field(env='POSTGRES_USER')
    ps_pwd: str = Field(env='POSTGRES_PASSWORD')
    ps_db: str = Field(env='POSTGRES_DB')
    ps_port: int = Field(env='POSTGRES_PORT')
    ps_url: str = Field(env='SQLALCHEMY_DATABASE_URI')

    class Config:
        env_file = 'config/.env.db'
