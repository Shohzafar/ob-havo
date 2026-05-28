import requests
from datetime import datetime

API_KEY = "a9520c4fbc4ae75a66b86e6bc5b87896"
BOT_TOKEN ="8526684512:AAHidDN8WUWJG2siZTt4n4M7cqABD_VgQdU" 

def get_weather_data(city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    r = requests.get(url)

    if r.status_code != 200:
        return f"❌ {city} topilmadi", False

    data = r.json()

    sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
    sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")

    description = data["weather"][0]["description"]

    text = f"""
📅 Bugun, {datetime.now().strftime('%A, %d-%B')}
📍 {city}

⛅ {description}

🌡 Temperatura: {data['main']['temp']}°C
🤒 Tuyuladi: {data['main']['feels_like']}°C

💧 Namlik: {data['main']['humidity']}%
🌬 Shamol: {data['wind']['speed']} m/s
📊 Bosim: {data['main']['pressure']} hPa

🌅 Quyosh chiqishi: {sunrise}
🌇 Quyosh botishi: {sunset}
"""
    return text, True


def get_weekly_weather(city: str):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    r = requests.get(url)

    if r.status_code != 200:
        return f"❌ {city} topilmadi"

    data = r.json()

    text = f"📅 {city} 5 kunlik ob-havo:\n\n"

    for item in data["list"][:5]:
        text += f"{item['dt_txt']} → {item['main']['temp']}°C\n"

    return text


def get_hourly_weather(city: str):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    r = requests.get(url)

    if r.status_code != 200:
        return f"❌ {city} topilmadi"

    data = r.json()

    text = f"⏰ {city} soatlik ob-havo:\n\n"

    for item in data["list"][:8]:
        time = item["dt_txt"][11:16]
        text += f"{time} → {item['main']['temp']}°C\n"

    return text