from pydantic import BaseSettings, Field


class DBSettings(BaseSettings):
    host: str = Field(env='DB_HOST')
    user: str = Field(env='DB_USER')
    password: str = Field(env='DB_PASSWORD')
    db: str = Field(env='DB_NAME')
    port: int = Field(default=5432, env='DB_PORT')

    class Config:
        env_file = ".env"

    @property
    def uri(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"

class Settings(BaseSettings):
    bot_token: str = Field(env='BOT_TOKEN')
    my_user_id: int = Field(env='MY_USER_ID')

    class Config:
        env_file = ".env"

db_settings = DBSettings()
settings = Settings()
