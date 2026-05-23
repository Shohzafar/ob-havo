from asyncio import run

from pymysql import IntegrityError
from aiogram import Bot, Dispatcher
from aiogram.filters.command import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from weather import get_weather_data
from db import db

TOKEN = "8694610807:AAH-kyMn5oiZif9b0rDPBYSYgXLcvm7MMj4"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# /start
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(text="Assalomu alaykum")
    try:
        db.register_user(
            telegram_id=str(message.from_user.id),
            fullname=message.from_user.full_name,
        )
        await message.answer(text="Muvaffaqiyatli ro'yxatga olindingiz")
    except IntegrityError:
        await message.answer(text="Qaytganingizdan xursandmiz")


# /delete_account
@dp.message(Command(commands=["delete_account"], prefix="/"))
async def delete_account(message: Message):
    telegram_id = message.from_user.id
    db.delete_user(telegram_id=telegram_id)
    await message.answer(
        text="Akkauntingiz ma'lumotlari muvaffaqiyatli o'chirildi"
    )


# /show_info
@dp.message(Command(commands=["show_info"], prefix="/"))
async def show_info(message: Message):
    telegram_id = message.from_user.id
    user = db.get_user(telegram_id=telegram_id)  # { "id": 1, "telegram_id": 123, "fullname": "..." }

    text = "--- Sizning ma'lumotlaringiz ---\n\n"
    text += f"ID: {user.get('id')}\n"
    text += f"Telegram ID: <code>{user.get('telegram_id')}</code>\n"
    text += f"FISh: <b>{user.get('fullname')}</b>"

    await message.answer(text=text, parse_mode="HTML")


# ...
@dp.message()
async def send_weather_data(message: Message):
    # import requests

    # url = f"https://youtube-video-fast-downloader-24-7.p.rapidapi.com/download_video/{message.text.split('=')[-1]}"

    # querystring = {"quality":"247"}

    # headers = {
    #     "x-rapidapi-key": "5b23da6f69mshe5cf01872e5597bp16c82bjsnd56e31e5ffd3",
    #     "x-rapidapi-host": "youtube-video-fast-downloader-24-7.p.rapidapi.com",
    #     "Content-Type": "application/json"
    # }

    # response = requests.get(url, headers=headers, params=querystring)
    # data = response.json()
    # print(data)
    # await message.answer_video(
    #     video=f"{data.get('file')}",
    #     caption="Marhamat!"
    # )


    weather_data, is_success = get_weather_data(city_name=message.text)

    markup = InlineKeyboardBuilder()
    markup.button(text="Shaharni saqlab qo'yish", callback_data=f"{message.text}")

    user_id = db.get_user(telegram_id=message.from_user.id).get('id')
    user_cities = db.get_user_cities(user_id=user_id)

    found = False
    for city in user_cities:
        if message.text == city.get('city_name'):
            found = True
            break

    if is_success and not found:
        await message.answer(
            text=weather_data,
            reply_markup=markup.as_markup(),
        )
    else:
        await message.answer(text=weather_data)


@dp.callback_query()
async def save_city(call: CallbackQuery):
    city_name = call.data
    user_id = db.get_user(telegram_id=call.from_user.id).get('id')

    try:
        db.add_city(user_id=user_id, city_name=city_name)

        markup = InlineKeyboardBuilder()
        markup.button(text="вњ… Shahar saqlandi", callback_data=f"{city_name}")
        await call.message.edit_reply_markup(
            reply_markup=markup.as_markup(),
        )
    except:
        await call.answer(text="Shahar qo'shilgan allaqachon", show_alert=True)
        return

    cities = db.get_user_cities(user_id=user_id)  # [ {'id': 1, 'user_id': 1, 'city_name': 'Toshkent'}, {...}, {...} ]

    markup = ReplyKeyboardBuilder()
    for city in cities:
        markup.button(text=city.get('city_name'))
    markup.adjust(2)

    await call.message.answer(
        text="Shahar muvaffaqiyatli qo'shildi вњ…",
        reply_markup=markup.as_markup(resize_keyboard=True),
    )


async def main():
    # Botni ishga tushirovchi funksiya
    db.create_users_table()
    db.create_cities_table()
    await dp.start_polling(bot)

run( main() )



