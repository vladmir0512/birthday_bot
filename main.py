import time
import requests
import json
from datetime import datetime as dt, date
from config import *

class BirthdayAlertBot:
    def __init__(self):
        self.twitch_token = None
        self.last_stream_status = False
        self.last_post_time = None

  

    def post_to_telegram(self, message):
        """Telegram оповещения о днях рождения!"""
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            
            # Очищаем сообщение от HTML тегов для безопасности
            clean_message = message.replace('<', '&lt;').replace('>', '&gt;')
            
            # Ограничиваем длину сообщения (Telegram лимит ~4096 символов)
            if len(clean_message) > 4000:
                clean_message = clean_message[:3997] + "..."
            
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": clean_message,
                "parse_mode": "HTML"
            }
            
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print("✅ Пост в Telegram успешно опубликован")
            else:
                # Получаем детали ошибки
                error_details = response.json() if response.content else "Нет деталей"
                print(f"❌ Ошибка постинга в Telegram: {response.status_code}")
                print(f"   Детали: {error_details}")
                
                # Попробуем отправить без HTML разметки
                if response.status_code == 400:
                    print("🔄 Пробуем отправить без HTML разметки...")
                    data["parse_mode"] = None
                    retry_response = requests.post(url, data=data)
                    if retry_response.status_code == 200:
                        print("✅ Пост в Telegram отправлен без HTML разметки")
                    else:
                        print(f"❌ Повторная ошибка: {retry_response.status_code}")
                
        except Exception as e:
            print(f"❌ Ошибка при постинге в Telegram: {e}")

    def check_birthday(self):
        current_day = date.today()
        BIRTHDAY_LIST = [
            "19.10.@darkqqw",
            "20.10.@GiltiasGoldenDragon"
        ]
        for i in BIRTHDAY_LIST:
            if str(current_day.month) == i.split(".")[1] and str(current_day.day) == i.split(".")[0]:
                self.post_to_telegram(f"Напоминаю, что сегодня {i.split(".")[0]}.{i.split(".")[1]} др {i.split(".")[2]}. Поздравьте!")
    
            elif str(current_day.month) == i.split(".")[1] and str(int(current_day.day) + 1) == i.split(".")[0]:
                self.post_to_telegram(f"Напоминаю, что завтра {i.split(".")[0]}.{i.split(".")[1]} др {i.split(".")[2]}. Не забудьте поздравить!")


    def run(self):
        """Основной цикл работы"""
        print("🚀 Запуск Telegram BirthdayAlertBot...")
        print(f"📱 Telegram канал: {TELEGRAM_CHAT_ID}")
        print("=" * 50)
        
        while True:
            try:
                self.check_birthday()
                time.sleep(6000)  # Проверяем каждую минуту
                
            except KeyboardInterrupt:
                print("\n🛑 Остановка программы...")
                break
            except Exception as e:
                print(f"❌ Неожиданная ошибка: {e}")
                time.sleep(60)

if __name__ == "__main__":
    bot = BirthdayAlertBot()
    bot.run()