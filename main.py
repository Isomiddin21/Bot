from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import logging
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API token from environment variable
API_TOKEN = os.getenv('API_TOKEN')

if not API_TOKEN:
    raise ValueError("No API_TOKEN provided. Please set the API_TOKEN environment variable.")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

# Messages dictionary
messages = {
    'start': {
        'en': "Choose your language:",
        'ru': "Выберите свой язык:",
        'uz': "Tilni tanlang:"
    },
    'sell_scooter': {
        'en': "Sell your scooter",
        'ru': "Продайте свой скутер",
        'uz': "Skuteringizni soting"
    },
    'upload_photo': {
        'en': "Upload a photo or press 'Finish'",
        'ru': "Загрузите фото или нажмите 'Завершить'",
        'uz': "Skuterni rasmini yuklang yoki 'Yakunlash' tugmasini bosing"
    },
    'ask_model': {
        'en': "Enter the model of your scooter",
        'ru': "Введите модель вашего скутера",
        'uz': "Skuteringiz modelini kiriting"
    },
    'ask_status': {
        'en': "Enter the condition of your scooter",
        'ru': "Введите состояние вашего скутера",
        'uz': "Skuteringiz holatini kiriting"
    },
    'ask_year': {
        'en': "Enter the year of your scooter ",
        'ru': "Введите год вашего скутера ",
        'uz': "Skuteringiz yilini kiriting "
    },
    'ask_distance': {
        'en': "Enter the distance covered by your scooter ",
        'ru': "Введите пройденное расстояние вашего скутера ",
        'uz': "Skuteringiz necha km yurganini kiriting "
    },
    'ask_price': {
        'en': "Enter the price of your scooter ",
        'ru': "Введите цену вашего скутера ",
        'uz': "Skuteringiz narxini kiriting "
    },
    'ask_location': {
        'en': "Enter the location of your scooter",
        'ru': "Введите местоположение вашего скутера",
        'uz': "Skuteringiz lokatsiyasini kiriting"
    },
    'ask_phone': {
        'en': "Enter your phone number ",
        'ru': "Введите ваш номер телефона ",
        'uz': "Telefon raqamingizni kiriting "
    },
    'confirmation': {
        'en': "Are all the entered details correct?",
        'ru': "Все введенные данные верны?",
        'uz': "Barcha kiritilgan ma'lumotlar to'g'rimi?"
    },
    'yes': {
        'en': "Yes",
        'ru': "Да",
        'uz': "Xa"
    },
    'no': {
        'en': "No",
        'ru': "Нет",
        'uz': "Yo'q"
    },
    'post_confirmation': {
        'en': "Your ad will be reviewed and posted soon on Skuter_Bozor channel.",
        'ru': "Ваше объявление будет проверено и скоро опубликовано на канале Skuter_Bozor.",
        'uz': "Sizning eloningiz ko'rib chiqiladi va tez orada @skuter_bozoruz kanalida e'lon qilinadi."
    },
    'invalid_year': {
        'en': "Invalid year. Please enter a year between 1950 and 2024.",
        'ru': "Неправильный год. Пожалуйста, введите год между 1950 и 2024.",
        'uz': "Noto'g'ri yil. Iltimos, 1950 va 2024 yillar orasidagi yilni kiriting."
    },
    'invalid_distance': {
        'en': "Invalid distance. Please enter a distance between 1 and 250000 km.",
        'ru': "Неправильное расстояние. Пожалуйста, введите расстояние между 1 и 250000 км.",
        'uz': "Noto'g'ri masofa. Iltimos, 1 va 250000 km orasidagi masofani kiriting."
    },
    'invalid_price': {
        'en': "Invalid price. Please enter a price between 1 and 100000$.",
        'ru': "Неправильная цена. Пожалуйста, введите цену между 1 и 100000$.",
        'uz': "Noto'g'ri narx. Iltimos, 1 va 100000$ orasidagi narxni kiriting."
    },
    'invalid_phone': {
        'en': "Invalid phone number. Please enter a phone number starting with +998 followed by 9 digits.",
        'ru': "Неправильный номер телефона. Пожалуйста, введите номер телефона, начинающийся с +998 и 9 цифр.",
        'uz': "Noto'g'ri telefon raqami. Iltimos, +998 bilan boshlanadigan va 9 ta raqamli telefon raqamini kiriting."
    }
}

locations = ['Andijon', 'Toshkent', 'Toshkent viloyati', 'Namangan', 'Fargona', 'Sirdaryo', 'Jizzax', 'Surxondaryo',
             'Qashqadaryo', 'Samarqand', 'Buxoro', 'Xorazm', 'Navoiy', 'Qoraqalpogiston']

# Function to create keyboards dynamically based on language
def create_keyboards(language='en'):
    language_buttons = {
        'en': {
            'sell_scooter': "Sell your scooter",
            'upload_photo': "Upload a photo",
            'finish': "Finish",
            'excellent': "Excellent",
            'good': "Good",
            'average': "Average",
            'bad': "Bad",
            'yes': "Yes",
            'no': "No"
        },
        'ru': {
            'sell_scooter': "Продайте свой скутер",
            'upload_photo': "Загрузите фото",
            'finish': "Завершить",
            'excellent': "Идеально",
            'good': "Хорошо",
            'average': "Среднее",
            'bad': "Плохо",
            'yes': "Да",
            'no': "Нет"
        },
        'uz': {
            'sell_scooter': "Skuteringizni soting",
            'upload_photo': "Skuterni rasmini yuklang",
            'finish': "Yakunlash",
            'excellent': "A'lo",
            'good': "Yaxshi",
            'average': "O'rtacha",
            'bad': "Yomon",
            'yes': "Xa",
            'no': "Yo'q"
        }
    }

    action_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    action_keyboard.add(KeyboardButton(language_buttons[language]['sell_scooter']))

    photo_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    photo_keyboard.add(
        KeyboardButton(language_buttons[language]['upload_photo']),
        KeyboardButton(language_buttons[language]['finish'])
    )

    status_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    status_keyboard.add(KeyboardButton(language_buttons[language]['excellent']),
                        KeyboardButton(language_buttons[language]['good']))
    status_keyboard.add(KeyboardButton(language_buttons[language]['average']),
                        KeyboardButton(language_buttons[language]['bad']))

    location_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    location_keyboard.add(*[KeyboardButton(location) for location in locations])

    confirmation_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    confirmation_keyboard.add(KeyboardButton(language_buttons[language]['yes']),
                              KeyboardButton(language_buttons[language]['no']))

    return action_keyboard, photo_keyboard, status_keyboard, location_keyboard, confirmation_keyboard


# Main function for user start interaction
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_data[message.from_user.id] = {'language': 'en'}  # default to English
    language_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    language_keyboard.add(KeyboardButton('English'), KeyboardButton('Русский'), KeyboardButton('O‘zbek'))
    await message.reply(messages['start']['en'], reply_markup=language_keyboard)


# Handler for language selection
@dp.message_handler(lambda message: message.text in ['English', 'Русский', 'O‘zbek'])
async def choose_language(message: types.Message):
    if message.text == 'English':
        user_data[message.from_user.id]['language'] = 'en'
    elif message.text == 'Русский':
        user_data[message.from_user.id]['language'] = 'ru'
    elif message.text == 'O‘zbek':
        user_data[message.from_user.id]['language'] = 'uz'

    lang = user_data[message.from_user.id]['language']
    action_keyboard, _, _, _, _ = create_keyboards(lang)

    await message.reply(messages['sell_scooter'][lang], reply_markup=action_keyboard)


# Handler for scooter selling action
@dp.message_handler(lambda message: message.text in ['Sell your scooter', 'Продайте свой скутер', 'Skuteringizni soting'])
async def sell_scooter(message: types.Message):
    lang = user_data[message.from_user.id]['language']
    _, photo_keyboard, _, _, _ = create_keyboards(lang)
    user_data[message.from_user.id]['photos'] = []

    await message.reply(messages['upload_photo'][lang], reply_markup=photo_keyboard)


# Handler for photo uploads
@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    lang = user_data[message.from_user.id]['language']
    user_data[message.from_user.id]['photos'].append(message.photo[-1].file_id)

    _, photo_keyboard, _, _, _ = create_keyboards(lang)
    await message.reply(messages['upload_photo'][lang], reply_markup=photo_keyboard)


# Handler for finishing photo uploads
@dp.message_handler(lambda message: message.text in ['Finish', 'Завершить', 'Yakunlash'])
async def finish_photos(message: types.Message):
    lang = user_data[message.from_user.id]['language']
    _, _, status_keyboard, _, _ = create_keyboards(lang)

    await message.reply(messages['ask_model'][lang])


# Handler for receiving scooter model
@dp.message_handler(lambda message: message.text and message.from_user.id in user_data and 'model' not in user_data[message.from_user.id])
async def receive_model(message: types.Message):
    lang = user_data[message.from_user.id]['language']
    user_data[message.from_user.id]['model'] = message.text

    _, _, status_keyboard, _, _ = create_keyboards(lang)
    await message.reply(messages['ask_status'][lang], reply_markup=status_keyboard)


# Handler for receiving scooter status
@dp.message_handler(lambda message: message.text in ['Excellent', 'Good', 'Average', 'Bad', 'Идеально', 'Хорошо', 'Среднее', 'Плохо', "A'lo", 'Yaxshi', "O'rtacha", 'Yomon'])
async def receive_status(message: types.Message):
    lang = user_data[message.from_user.id]['language']
    user_data[message.from_user.id]['status'] = message.text

    await message.reply(messages['ask_year'][lang])


# Handler for receiving scooter year
@dp.message_handler(lambda message: re.match(r'^\d{4}$', message.text))
async def receive_year(message: types.Message):
    lang = user_data[message.from_user.id]['language']
    year = int(message.text)
    if 1950 <= year <= 2024:
        user_data[message.from_user.id]['year'] = year
        await message.reply(messages['ask_distance'][lang])
    else:
        await message.reply(messages['invalid_year'][lang])


# Handler for receiving distance
@dp.message_handler(lambda message: re.match(r'^\d+$', message.text))
async def receive_distance(message: types.Message):
    lang = user_data[message.from_user.id]['language']
    distance = int(message.text)
    if 1 <= distance <= 250000:
        user_data[message.from_user.id]['distance'] = distance
        await message.reply(messages['ask_price'][lang])
    else:
        await message.reply(messages['invalid_distance'][lang])


# Handler for receiving price
@dp.message_handler(lambda message: re.match(r'^\d+$', message.text))
async def receive_price(message: types.Message):
    lang = user_data[message.from_user.id]['language']
    price = int(message.text)
    if 1 <= price <= 100000:
        user_data[message.from_user.id]['price'] = price

        _, _, _, location_keyboard, _ = create_keyboards(lang)
        await message.reply(messages['ask_location'][lang], reply_markup=location_keyboard)
    else:
        await message.reply(messages['invalid_price'][lang])


# Handler for receiving location
@dp.message_handler(lambda message: message.text in locations)
async def receive_location(message: types.Message):
    lang = user_data[message.from_user.id]['language']
    user_data[message.from_user.id]['location'] = message.text
    await message.reply(messages['ask_phone'][lang])


# Handler for receiving phone number
@dp.message_handler(lambda message: re.match(r'^\+998\d{9}$', message.text))
async def receive_phone(message: types.Message):
    lang = user_data[message.from_user.id]['language']
    phone_number = message.text
    if re.match(r'^\+998\d{9}$', phone_number):
        user_data[message.from_user.id]['phone'] = phone_number
        _, _, _, _, confirmation_keyboard = create_keyboards(lang)
        await message.reply(messages['confirmation'][lang], reply_markup=confirmation_keyboard)
    else:
        await message.reply(messages['invalid_phone'][lang])


# Handler for final confirmation
@dp.message_handler(lambda message: message.text in ['Yes', 'No', 'Да', 'Нет', 'Xa', "Yo'q"])
async def final_confirmation(message: types.Message):
    lang = user_data[message.from_user.id]['language']
    if message.text in ['Yes', 'Да', 'Xa']:
        await message.reply(messages['post_confirmation'][lang])
    else:
        await message.reply("Let's start over. " + messages['sell_scooter'][lang])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)













