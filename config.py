import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()


class Config:
    """Конфигурационный класс для бота и API."""

    # Telegram Bot
    BOT_TOKEN = os.getenv("BOT_TOKEN", "default_bot_token")

    # Белый список пользователей (если пусто — ставим [])
    ALLOWED_USERS = os.getenv("ALLOWED_USERS", "")
    if ALLOWED_USERS:
        ALLOWED_USERS = list(map(int, ALLOWED_USERS.split(",")))
    else:
        ALLOWED_USERS = []

    # API IMEI Check
    IMEI_CHECK_API_URL = "https://api.imeicheck.net/v1"
    IMEI_CHECK_TOKEN = os.getenv("IMEI_CHECK_TOKEN", "default_imei_token")
    SERVICE_ID = 12  # ID тестового сервиса

    # API Авторизация
    API_TOKEN = os.getenv("API_TOKEN", "default_api_token")

    # Настройки API-запросов
    RETRY_ATTEMPTS = 3  # Количество попыток при ошибках
    RETRY_DELAY = 2  # Задержка перед повторным запросом (сек)
