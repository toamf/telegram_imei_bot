import asyncio
import json
import logging
from typing import Dict

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import ClientSession, ClientError
from stdnum.imei import is_valid

from config import Config

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=Config.BOT_TOKEN)
dp = Dispatcher()


async def fetch_imei_info(imei: str) -> Dict:
    """Запрашивает данные об IMEI через API."""
    url = f"{Config.IMEI_CHECK_API_URL}/checks"
    headers = {
        "Authorization": f"Bearer {Config.IMEI_CHECK_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = json.dumps({
        "deviceId": imei,
        "serviceId": Config.SERVICE_ID
    })

    async with ClientSession() as session:
        try:
            async with session.post(url, headers=headers, data=payload) as response:
                response_text = await response.text()
                logger.info(f"API Response (POST): {response.status} - {response_text}")

                if response.status == 201:
                    response_json = await response.json()
                    check_id = response_json.get("id")

                    if check_id:
                        results = await asyncio.gather(get_imei_result(check_id))
                        return results[0]

                return {"error": f"Ошибка API: {response.status}, {response_text}"}
        except ClientError as e:
            logger.error(f"Ошибка соединения с API: {e}")
            return {"error": "Ошибка соединения с API"}


async def get_imei_result(check_id: str) -> Dict:
    """Получает результат проверки IMEI по ID."""
    url = f"{Config.IMEI_CHECK_API_URL}/checks/{check_id}"
    headers = {
        "Authorization": f"Bearer {Config.IMEI_CHECK_TOKEN}",
        "Content-Type": "application/json"
    }

    async with ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:
                response_text = await response.text()
                logger.info(f"API Response (GET): {response.status} - {response_text}")

                if response.status == 200:
                    return await response.json()

                return {"error": f"Ошибка API при получении результата: {response.status}, {response_text}"}
        except ClientError as e:
            logger.error(f"Ошибка соединения с API: {e}")
            return {"error": "Ошибка соединения с API"}


@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Приветственное сообщение."""
    if message.from_user.id not in Config.ALLOWED_USERS:
        await message.answer("🚫 У вас нет доступа к этому боту.")
        return
    await message.answer("🔍 Отправьте IMEI для проверки.")


@dp.message(F.text)
async def handle_imei(message: Message):
    """Обрабатывает IMEI, если это текстовое сообщение."""
    if message.from_user.id not in Config.ALLOWED_USERS:
        await message.answer("🚫 У вас нет доступа к этому боту.")
        return

    imei = message.text.strip()

    # Проверка валидности IMEI
    if not is_valid(imei):
        await message.answer("❌ Некорректный IMEI. Проверьте и попробуйте снова.")
        return

    await bot.send_chat_action(message.chat.id, action="typing")
    imei_info = await fetch_imei_info(imei)

    if "error" in imei_info:
        await message.answer(f"⚠ Ошибка: {imei_info['error']}")
        return

    properties = imei_info.get("properties", {})
    response = (
        f"📱 Информация по IMEI {imei}:\n"
        f"🔹 Устройство: {properties.get('deviceName', 'Неизвестно')}\n"
        f"🔹 Серийный номер: {properties.get('serial', 'Неизвестно')}\n"
        f"🔹 Страна покупки: {properties.get('purchaseCountry', 'Неизвестно')}\n"
        f"🔹 FMI: {'✅ Включен' if properties.get('fmiOn', False) else '❌ Выключен'}\n"
        f"🔹 Чёрный список GSMA: {'🚨 В списке' if properties.get('gsmaBlacklisted', False) else '✅ Чистый'}\n"
    )
    await message.answer(response)


@dp.message()
async def unknown_message(message: Message):
    """Отвечает на неизвестные сообщения (например, фото, документы, видео)."""
    await message.answer("🚫 Пожалуйста, отправьте IMEI в виде текста.")


async def main():
    """Запуск бота."""
    logger.info("Запуск Telegram-бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
