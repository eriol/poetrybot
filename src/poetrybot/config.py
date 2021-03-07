"""Configuration module for poetrybot."""

import environ


@environ.config(prefix="")
class Config:
    TELEGRAM_TOKEN = environ.var()
    DATABASE_URL = environ.var()
