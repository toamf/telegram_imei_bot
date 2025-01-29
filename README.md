# **Telegram IMEI Bot & API**

## **Описание**
Этот проект представляет собой **Telegram-бот** и **API**, которые позволяют проверять **IMEI-устройства** через сервис **IMEI Check**.

Проект включает:
- **Telegram-бот** (`bot.py`) для пользователей, отправляющих IMEI.
- **API-сервер** (`api.py`) с защищенной авторизацией для внешних запросов.
- **Интеграцию с сервисом [IMEI Check](https://imeicheck.net/)**.

## **Стек технологий**
- **Python 3.10+**
- **Aiogram 3.17.0** (для Telegram-бота)
- **FastAPI 0.115.7** (для API)
- **Aiohttp 3.11.11** (для асинхронных запросов)
- **Uvicorn 0.34.0** (для запуска API)
- **Dotenv 1.0.1** (для работы с переменными окружения)

---

## **Установка и запуск проекта**

### **1️⃣ Клонирование репозитория**
```bash
git clone https://github.com/toamf/telegram_imei_bot.git
cd telegram_imei_bot
```

### **2️⃣ Создание виртуального окружения**
```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux/macOS
venv\Scripts\activate     # Для Windows
```

### **3️⃣ Установка зависимостей**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### **4️⃣ Создание `.env` файла**
Создайте `.env` в корневой папке проекта и добавьте свои API-ключи:

```ini
# Токен Telegram-бота
BOT_TOKEN=

# Токен API для авторизации внешних запросов
API_TOKEN=

# Токен для работы с сервисом IMEI Check
IMEI_CHECK_TOKEN=

# Белый список пользователей Telegram (ID через запятую)
ALLOWED_USERS=123456789,987654321
```

---

## **Запуск проекта**

### **1️⃣ Запуск Telegram-бота**
```bash
python bot.py
```

### **2️⃣ Запуск API-сервера**
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

API будет доступен по адресу:
```
http://localhost:8000
```

---

## **Проверка API**

### **1️⃣ Тестовый запрос через `curl`**
```bash
curl -X POST http://localhost:8000/api/check-imei \
-H "Authorization: Bearer TOKEN" \
-H "Content-Type: application/json" \
-d '{"imei": "356735111052198"}'
```

### **2️⃣ Тестовый запрос через Python**
```python
import requests
import json

url = "http://localhost:8000/api/check-imei"
headers = {
    "Authorization": "Bearer TOKEN",
    "Content-Type": "application/json"
}
payload = json.dumps({"imei": "356735111052198"})

response = requests.post(url, headers=headers, data=payload)
print(response.status_code, response.json())
```

### **3️⃣ Тестовый запрос через Postman**
- Метод: `POST`
- URL: `http://localhost:8000/api/check-imei`
- **Headers**:
  - `Authorization: Bearer TOKEN`
  - `Content-Type: application/json`
- **Body (raw, JSON)**:
  ```json
  {
    "imei": "356735111052198"
  }
  ```

---

## **Ответ API**
Если API работает правильно, ответ будет в формате JSON:
```json
{
  "deviceId": "356735111052198",
  "deviceName": "iPhone SE (A2782)",
  "serial": "7NAW8L6SIEL6WP",
  "purchaseCountry": "United States",
  "fmiOn": false,
  "lostMode": true,
  "network": "Global"
}
```

---

## **Возможные ошибки**
| Код | Ошибка | Причина |
|-----|--------|---------|
| `401` | `"Unauthorized"` | Неверный API-токен |
| `400` | `"Invalid IMEI"` | Некорректный формат IMEI |
| `500` | `"Internal Server Error"` | Ошибка на стороне сервера |

---
