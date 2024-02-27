import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = ''
    SECRET_KEY: str = secrets.token_urlsafe(32)
    X_API_TOKEN: str = 'no-secret-yet'

    PROJECT_NAME: str = 'fstracker'

    TG_BOT_TOKEN: str = '6571737224:AAFUll25HC2vSQ40W2HvCzcLg0v7rbYXkiI'
    TG_API_ID: str = '23269565'
    TG_API_HASH: str = '98aaa94473b7ce1e88fc28234d85b936'
    TG_SESSION_NAME: str = 'fstracker_session'

    class Config:
        case_sensitive = True


settings = Settings()
