import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

# Telegram Config
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')