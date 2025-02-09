from pydantic.v1 import BaseSettings


class Config(BaseSettings):
    MYSQL_DATABASE: str = "shopping_service"
    MYSQL_USER: str = "user"
    MYSQL_PASSWORD: str = "123456"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: str = "3309"
    DATABASE_URL: str = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    REDIS_HOST: str = "localhost"
    REDIS_PORT: str = "6381"
    REDIS_TTL: int = 60*60
    SECRET_KEY: str = "secret_key"
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRY_TIME: float = 120.0
    BASE_URL = "http://localhost:8000"
    OPENAI_API_KEY = ""
