import os
import random
import asyncio
import logging

from aiogram import Bot, Dispatcher, executor, types

from weather import get_weather
from config.config import TOKEN
from texts import HELLO, HELLO_2, good_phrases


logging.basicConfig(level=logging.INFO,
                    filename='data/log.log', 
                    encoding='utf-8', 
                    )


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = HELLO.format(user_name)
    
    logging.info(f"{user_name=} {user_id=} sent message: {message.text}")
    await message.reply(text)
    
    await asyncio.sleep(4)
    text = 'Например вот так:\n*Фетхие, завтра*'
    await bot.send_message(user_id, text, parse_mode='Markdown')
    
    await asyncio.sleep(3)
    text = HELLO_2
    await bot.send_message(user_id, text, parse_mode='Markdown')


@dp.message_handler()
async def send_echo(message: types.Message):
    user_firstname = message.from_user.first_name
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    city = message.text
    logging.info(f"{user_name=} {user_id=} sent message: {city}")
    
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
    await bot.send_message(user_id, forecast, parse_mode='Markdown')
    

if __name__ == '__main__':
    executor.start_polling(dp)