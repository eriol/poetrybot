"""Configuration module for poetrybot."""

import environ


@environ.config(prefix="")
class Config:
    AUTH_TOKEN = environ.var()
    DATABASE_URL = environ.var()
    TELEGRAM_TOKEN = environ.var()
