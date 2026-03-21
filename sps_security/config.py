"""
config.py
Configuração central do sistema
"""

import os


class Config:

    # API KEYS
    VIRUSTOTAL_API_KEY = "3fc47d76d43b153c64f55571a83651778c3c8104a7735588b82d1cd965777b23"

    # LIMITES
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

    # TIMEOUTS
    API_TIMEOUT = 15

    # CACHE
    ENABLE_CACHE = True

    # LOG
    DEBUG = True
