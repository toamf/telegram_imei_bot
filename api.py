import logging

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from stdnum.imei import is_valid

from config import Config
from main import fetch_imei_info

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Создание FastAPI-приложения
app = FastAPI(title="IMEI Check API", description="API для проверки IMEI устройств", version="1.0")


# Модель запроса
class IMEIRequest(BaseModel):
    imei: str


@app.get("/")
async def root():
    """Тестовый эндпоинт"""
    return {"message": "IMEI Check API is running"}


@app.post("/api/check-imei")
async def check_imei(request_data: IMEIRequest, authorization: str = Header(None)):
    """API-эндпоинт для проверки IMEI"""

    # Проверяем токен авторизации
    if authorization != f"Bearer {Config.API_TOKEN}":
        logger.warning("Ошибка авторизации: неверный токен")
        raise HTTPException(status_code=401, detail="Unauthorized")

    imei = request_data.imei.strip()

    # Проверяем, валиден ли IMEI
    if not is_valid(imei):
        logger.warning(f"Ошибка: Неверный IMEI - {imei}")
        raise HTTPException(status_code=400, detail="Invalid IMEI")

    # Отправляем запрос в API IMEI Check
    imei_info = await fetch_imei_info(imei)

    if "error" in imei_info:
        logger.error(f"Ошибка API при проверке IMEI: {imei_info['error']}")
        raise HTTPException(status_code=500, detail=imei_info["error"])

    return imei_info
