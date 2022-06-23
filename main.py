import requests
from datetime import datetime
from config import OPEN_TOKEN, BOT_TOKEN
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


emojis_code = {
    'clear sky': 'Clear sky \U0001F30C',
    'few clouds': 'Few clouds \U0001F324',
    'scattered clouds': 'Scattered clouds \U0001F325',
    'broken clouds': 'Broken clouds \U0001F325',
    'overcast clouds': 'Broken clouds \U0001F325',
    'shower rain': 'Shower rain \U0001F326',
    'rain': 'Rain \U0001F327',
    'thunderstorm': 'Thunderstorm \U0001F329',
    'snow': 'Snow \U0001F328',
    'mist': 'Mist \U0001F32B',
}


bot = Bot(token=BOT_TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Hello! I am Fast Weather Bot \U0001F31A \U0001F308	. \n To find out the weather in your '
                        'city - enter the name of the city: ')


@dispatcher.message_handler()
async def get_weather(message: types.Message, token=OPEN_TOKEN):
    try:
        info = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={token}&units=metric'
        )
        data = info.json()

        weather = data['weather'][0]['description']
        if weather in emojis_code:
            weather = emojis_code[weather]

        answer = f"Hello! Actual weather for city {data['name']} now - at {datetime.now().strftime('%Y-%m-%d %H:%M')} is: \n" \
                 f"temperature: {data['main']['temp']} \U0001F321 \n" \
                 f"it feels like: {data['main']['feels_like']} \U0001F92B \n" \
                 f"by the way the weather is - {weather}. \n" \
                 f"Have a nice day! \U0001F917"
        await message.reply(answer)
    except:
        await message.reply('Can not find such city! Try another one.')


if __name__ == '__main__':
    executor.start_polling(dispatcher)
