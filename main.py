import os, time, requests, telebot, threading

TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_URL = "https://githubusercontent.com"
users = set()
last_weather = None

WEATHER_TRANSLATION = {
    "Clear": "☀️ Ясно (Обычная погода)",
    "Rain": "🌧 Дождь",
    "Cold": "🥶 Холод",
    "Meteor Shower": "💫 Звездопад",
    "Rainbow Weather": "🌈 Радужная погода",
    "Rainbow Moon": "🦄 Радужная луна",
    "Golden Moon": "💛 Золотая луна",
    "Blood Moon": "🛑 Кровавая луна",
    "Thunderstorm": "⚡️ Гроза",
    "Aurora": "🌌 Аврора (Северное сияние)",
    "Mega Moon": "🌕 Мега луна"
}

def check_game():
    global last_weather
    if not TOKEN: return
    try:
        res = requests.get(API_URL, timeout=10).json()
        current_weather = res.get("weather", "Clear")
        if current_weather != last_weather:
            last_weather = current_weather
            ru_weather = WEATHER_TRANSLATION.get(current_weather, f"❓ Новая погода ({current_weather})")
            text = f"🌤 В GROW A GARDEN 2 СМЕНИЛАСЬ ПОГОДА!\n\nСейчас в игре: {ru_weather}"
            for user_id in list(users):
                try: bot.send_message(user_id, text)
                except: pass
    except: pass

def loop_check():
    while True:
        check_game()
        time.sleep(60)

if TOKEN:
    threading.Thread(target=loop_check, daemon=True).start()
    while True:
        try:
            bot = telebot.TeleBot(TOKEN)
            @bot.message_handler(commands=['start'])
            def start_cmd(message):
                users.add(message.chat.id)
                bot.send_message(message.chat.id, "✅ Ты подписался на мгновенные уведомления о ПОГОДЕ в Grow a Garden 2!")
            bot.polling(none_stop=True, timeout=60)
        except: time.sleep(10)
else:
    while True: time.sleep(3600)
