import os
import asyncio
import logging
import random

from aiogram import Bot, Dispatcher, executor, types

from weather import get_weather
from config.config import TOKEN
from texts import HELLO_0, HELLO_1, HELLO_2, good_phrases

logging.basicConfig(level=logging.INFO,
                    filename='data/log.log', 
                    encoding='utf-8', 
                    )


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

admin_id = int(os.getenv('ADMIN_ID'))

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = HELLO_0.format(user_name)
    
    if user_id != admin_id:
        await bot.send_message(admin_id, f'{user_name=} {user_id=}',
                               parse_mode='Markdown')
    
    logging.info(f"{user_name=} {user_id=} sent message: {message.text}")
    await message.reply(text)

    for phrase in HELLO_1, HELLO_2:
        await asyncio.sleep(3)
        await bot.send_message(user_id, phrase, parse_mode='Markdown')
    

@dp.message_handler()
async def send_echo(message: types.Message):
    user_firstname = message.from_user.first_name
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    city = message.text
    logging.info(f"{user_name=} {user_id=} sent message: {city}")
    
    if user_id != admin_id:
        await bot.send_message(admin_id, f'{user_name=} {user_id=} {city=}',
                               parse_mode='Markdown')
    
    day = ''
    try:
        city, day = city.split(', ')
    except Exception as e:
        logging.info(f"{user_name=} {user_id=} Exception {e}")
    
    temp = await get_weather(city, day)
    if temp == 404:
        await bot.send_message(user_id, 'Ничего не нашёл! Введи имя города заново 💔')
        
    phrase = random.choice(good_phrases)

    logging.info(f"{user_name=} {user_id=} {temp=}")
    forecast = '\n ・'.join(temp) + ' 💜' + f'\n\n{phrase} ✨'.format(user_firstname)
    await bot.send_message(user_id, forecast, 
                           parse_mode='Markdown',          # to use bold and etc.
                           disable_web_page_preview=True)  # if u don't
    

if __name__ == '__main__':
    executor.start_polling(dp)
