from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # database
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    
    #oauth2
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    class Config:
        env_file = ".env"
    
settings = Settings()