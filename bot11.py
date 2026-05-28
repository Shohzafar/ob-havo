from asyncio import run

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, 
    ReplyKeyboardMarkup, KeyboardButton
)
from weather5 import get_hourly_weather, get_weather_data, get_weekly_weather
from db3 import db

TOKEN ="8526684512:AAHidDN8WUWJG2siZTt4n4M7cqABD_VgQdU" 
API_TOKEN = "a9520c4fbc4ae75a66b86e6bc5b87896"

bot = Bot(token=TOKEN)
dp = Dispatcher()

user_state = {}
user_mode = {}
selected_city = {}

# =========================
# KEYBOARD BUILDER
# =========================
def make_reply(rows):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=t) for t in row] for row in rows],
        resize_keyboard=True
    )

# =========================
# REGION KEYBOARD
# =========================
regions_keyboard = make_reply([
    ["Farg'ona", "Andijon", "Namangan"],
    ["Toshkent", "Toshkent Shahri", "Samarqand"],
    ["Buxoro", "Xorazm", "Jizzax"],
    ["Qashqadaryo", "Surxondaryo", "Sirdaryo"]
])
# =========================
# DISTRICTS KEYBOARDS
# =========================
Fargona_keyboard = make_reply([
    ["Buvayda", "Uchko'prik", "Quva"],
    ["So'x", "Farg'ona", "O'zbekiston"],
    ["Furqat", "Bag'dod", "Beshariq"],
    ["Rishton", "Yozyovon", "Dang'ara"]
])

Andijon_keyboard = make_reply([
    ["Asaka", "Baliqchi", "Bo'ston"],
    ["Buloqboshi", "Izboskan", "Jalaquduq"],
    ["Marhamat", "Oltinko'l", "Paxtaobod"],
    ["Shahrixon", "Xo'jaobod", "Qo'rg'ontepa"]
])

Namangan_keyboard = make_reply([
    ["Chortoq", "Chust", "Kosonsoy"],
    ["Mingbuloq", "Norin", "Pop"],
    ["To'raqo'rg'on", "Uychi", "Uchqo'rg'on"]
])

Toshkent_keyboard = make_reply([
    ["Bekobod", "Bo'ka", "Chinoz"],
    ["Qibray", "Ohangaron", "Parkent"],
    ["Yangiyo'l", "Zangiota", "Piskent"],
    ["Yuqori Chirchiq", "Quyi Chirchiq"],
    ["Oq Qo'rg'on", "Bo'stonliq"]
])

Toshkent_city_keyboard = make_reply([
    ["Yashnobod", "Olmazor", "Chilonzor"],
    ["Mirobod", "Yakkasaroy", "Sergeli"],
    ["Yunusobod", "Shayxontoxur", "Uchtepa"],
    ["Mirzo Ulug'bek", "Bektemir"]
])

Samarqand_keyboard = make_reply([
    ["Oqdaryo", "Bulung'ur", "Kattaqo'rg'on"],
    ["Pastarg'om", "Paxtachi", "Ishtixon"],
    ["Urgut", "Toyloq", "Nurobod"],
    ["Payariq", "Narpay", "Qo'shrabot"]
])

Buxoro_keyboard = make_reply([
    ["Qora Ko'l", "Romitan", "Peshku"],
    ["G'ijduvon", "Kogon", "Olot"],
    ["Qorovulbozor", "Buxoro", "Vobkent"],
    ["Jondor", "Shofirkon"]
])

Xorazm_keyboard = make_reply([
    ["Bog'ot", "Gurlan", "Hazorasp"],
    ["Xiva", "Qo'shko'pir", "Shovot"],
    ["Urganch", "Xonqa", "Yangibozor"],
    ["Tuproq Qala", "Yangi Ariq"]
])

Jizzax_keyboard = make_reply([
    ["Arnasoy", "Baxmal", "Do'stlik"],
    ["Forish", "G'allaorol", "Zomin"],
    ["Paxtakor", "Zarbdor", "Zafarobod"],
    ["Sharof Rashidov", "Yangiobod", "Mirzacho'l"]
])

Qashqadaryo_keyboard = make_reply([
    ["Chiroqchi", "Dehqonobod", "G'uzor"],
    ["Kasbi", "Kitob", "Koson"],
    ["Mirishkor", "Muborak", "Nishon"],
    ["Qamashi", "Qarshi", "Bahoriston"],
    ["Ko'kdala", "Qarshi shahri", "Yakkabog'"],
    ["Shahrisabz"]
])

Surxondaryo_keyboard = make_reply([
    ["Angor", "Sho'rchi", "Boysun"],
    ["Denov", "Jarqo'rg'on", "Sherobod"],
    ["Muzrabot", "Qumqo'rg'on", "Qiziriq"],
    ["Oltinsoy", "Sariosiyo", "Termiz"]
])

Sirdaryo_keyboard = make_reply([
    ["Boyovut", "Guliston", "Mirzaobod"],
    ["Oqoltin", "Sayxunobod", "Sardoba"],
    ["Sirdaryo", "Xovos"]
])

# =========================
# MAP
# =========================
region_map = {
    "Farg'ona": Fargona_keyboard,
    "Andijon": Andijon_keyboard,
    "Namangan": Namangan_keyboard,
    "Toshkent": Toshkent_keyboard,
    "Toshkent Shahri": Toshkent_city_keyboard,
    "Samarqand": Samarqand_keyboard,
    "Buxoro": Buxoro_keyboard,
    "Xorazm": Xorazm_keyboard,
    "Jizzax": Jizzax_keyboard,
    "Qashqadaryo": Qashqadaryo_keyboard,
    "Surxondaryo": Surxondaryo_keyboard,
    "Sirdaryo": Sirdaryo_keyboard,
}

@dp.message(CommandStart())
async def start(message: Message):
    user_state[message.from_user.id] = "name"

    await message.answer(
        "Assalomu alaykum ob-havo botimizga xush kelibsiz sizga qanday murojaat qilsak bo'ladi 🚀\nIsmingizni kiriting:"
    )
@dp.message()
async def handler(message: Message):
    user_id = message.from_user.id
    text = message.text

    if not text:
        return

    state = user_state.get(user_id)

    # ========== NAME ==========
    if state == "name":
        user_state[user_id] = "region"
        await message.answer(
            f"Rahmat {text} ✅\nHududingizni tanlang 👇",
            reply_markup=regions_keyboard
        )
        return

    # ========== REGION ==========
    if state == "region":
        if text in region_map:
            user_state[user_id] = "district"
            await message.answer(
                "Tumanni tanlang 👇",
                reply_markup=region_map[text]
            )
        return

    # ========== DISTRICT ==========
    if state == "district":
        if text in all_districts:
            selected_city[user_id] = text
            user_state[user_id] = "weather"

            await message.answer(
                f"Assalomu alaykum shohzafar Ob-havo botiga hush kelibsiz 🚀 Bu bot orqali O'zbekistonnig barcha hududlaridagi ob-havo ma'lumotini ko'rishingiz mumkin. Bot sizga foyda keltirsa biz hursand bo'lamiz. Bot orqali siz, hududingizdagi 3 xil obhavo ma'lumotni bilishingiz mumkin 1️⃣ Hozirgi ob-havo (to'liq ma'lumot) 2️⃣ Haftalik ob-havo 3️⃣ Soatlik ob-havo 📩 Takliflaringiz bo'lsa @shohzafar2006 ga yuborishingiz mumkin. Foydali deb bilgan bo'lsangiz yaqinlaringizga ham ulashing Doimiy ob-havo ma'lumotlari 👉 Ob-havo BOT (@WEATHER_UNKNOWN_BOT)",
                reply_markup=Third_keyboard
            )
        return

    # ========== CHANGE REGION ==========
    if text == "🔄 Hududni o'zgartirish":
        user_state[user_id] = "region"
        await message.answer(
            "Hududingizni tanlang 👇",
            reply_markup=regions_keyboard
        )
        return

    # ========== WEATHER ==========
    if state == "weather":

     city = selected_city.get(user_id)

    if not city:
        await message.answer("❌ Avval tumanni tanlang")
        return

    # ================= BUGUN =================
    if text in ["⛅ Hozirgi ob-havo", "/bugun"]:
        await message.answer("⏳ Yuklanmoqda...")
        weather, ok = get_weather_data(city)

        if not ok:
            await message.answer(weather)
            return

        await message.answer(weather)
        return

    # ================= HAFTALIK =================
    elif text in ["📅 Haftalik ob-havo", "/haftalik"]:
        await message.answer("⏳ Yuklanmoqda...")
        weather = get_weekly_weather(city)

        await message.answer(weather)
        return

    # ================= SOATLIK =================
    elif text in ["⏰ Soatlik ob-havo", "/soatlik"]:
        await message.answer("⏳ Yuklanmoqda...")
        weather = get_hourly_weather(city)

        await message.answer(weather)
        return

    # ================= STATS =================
    elif text == "/stats":
        await message.answer(
            f"📊 Bot statistikasi:\n"
            f"👤 User ID: {user_id}\n"
            f"🏙 Tanlangan shahar: {city}\n"
            f"📌 Holat: {state}"
        )
        return
    elif text == "📞 Aloqa":
        await message.answer("Assalomu alaykum shohzafar Ob-havo botiga hush kelibsiz 🚀 Bu bot orqali O'zbekistonnig barcha hududlaridagi ob-havo ma'lumotini ko'rishingiz mumkin. Bot sizga foyda keltirsa biz hursand bo'lamiz. Bot orqali siz, hududingizdagi 3 xil obhavo ma'lumotni bilishingiz mumkin 1️⃣ Hozirgi ob-havo (to'liq ma'lumot) 2️⃣ Haftalik ob-havo 3️⃣ Soatlik ob-havo 📩 Takliflaringiz bo'lsa @shohzafar2006 ga yuborishingiz mumkin. Foydali deb bilgan bo'lsangiz yaqinlaringizga ham ulashing Doimiy ob-havo ma'lumotlari 👉 Ob-havo BOT (@WEATHER_UNKNOWN_BOT)")
    # ================= DEFAULT =================
    else:
        await message.answer("❗ Noto‘g‘ri buyruq")
        return
Third_keyboard = make_reply([
    ["⛅ Hozirgi ob-havo", "📅 Haftalik ob-havo"],
    ["⏰ Soatlik ob-havo", "🔄 Hududni o'zgartirish"],
    ["📞 Aloqa"]
])
all_districts = { "Buvayda","Uchko'prik","Quva",
 "So'x","Farg'ona","O'zbekiston",
 "Furqat","Bag'dod","Beshariq", 
 "Rishton","Yozyovon","Dang'ara",
 "Asaka","Baliqchi","Bo'ston",
 "Buloqboshi","Izboskan", "Jalaquduq",
 "Marhamat","Oltinko'l","Paxtaobod","Shahrixon","Xo'jaobod",
 "Qo'rg'ontepa", "Chortoq","Chust","Kosonsoy","Mingbuloq","Norin",
 "Pop","To'raqo'rg'on","Uychi","Uchqo'rg'on", "Bekobod",
 "Bo'ka","Chinoz","Qibray","Ohangaron","Parkent","Yangiyo'l",
 "Zangiota","Piskent", "Yuqori Chirchiq","Quyi Chirchiq","Oq Qo'rg'on","Bo'stonliq", 
 "Yashnobod","Olmazor","Chilonzor","Mirobod","Yakkasaroy","Sergeli","Yunusobod","Shayxontoxur",
 "Uchtepa", "Mirzo Ulug'bek","Bektemir", "Oqdaryo",
 "Bulung'ur","Kattaqo'rg'on","Pastarg'om","Paxtachi","Ishtixon",
 "Urgut","Toyloq","Nurobod", "Payariq","Narpay","Qo'shrabot", "Qora Ko'l",
 "Romitan","Peshku","G'ijduvon","Kogon","Olot","Qorovulbozor","Buxoro","Vobkent", 
 "Jondor","Shofirkon", "Bog'ot","Gurlan","Hazorasp","Xiva","Qo'shko'pir","Shovot","Urganch","Xonqa","Yangibozor", 
 "Tuproq Qala","Yangi Ariq", "Arnasoy","Baxmal","Do'stlik","Forish","G'allaorol","Zomin","Paxtakor","Zarbdor","Zafarobod", 
 "Sharof Rashidov","Yangiobod","Mirzacho'l", "Chiroqchi","Dehqonobod","G'uzor","Kasbi","Kitob","Koson","Mirishkor","Muborak",
 "Nishon", "Qamashi","Qarshi","Bahoriston","Ko'kdala","Qarshi shahri","Yakkabog'","Shahrisabz", "Angor","Sho'rchi","Boysun","Denov",
 "Jarqo'rg'on","Sherobod","Muzrabot","Qumqo'rg'on","Qiziriq", "Oltinsoy","Sariosiyo","Termiz", "Boyovut","Guliston","Mirzaobod",
 "Oqoltin","Sayxunobod","Sardoba","Sirdaryo","Xovos" }
async def main():
    db.create_users_table()
    db.create_cities_table()
    await dp.start_polling(bot)

run(main())