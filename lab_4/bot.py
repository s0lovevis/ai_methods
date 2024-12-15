import logging
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import asyncio

# Инициализация логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего Telegram-бота
TELEGRAM_TOKEN = "7604679620:AAFb9Gs3wCca1PEcLMF4j8ENfNaqbfhgddQ"

# Создание экземпляра бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
router = Router()

# Заглушка для ответа модели
async def mock_model_response(ingredients: str, country: str, cooking_time: str) -> str:
    return f"Рецепт для ингредиентов: {ingredients}, страны: {country}, время готовки: {cooking_time}."

# Словарь для хранения данных пользователя
user_data = {}

# Обработчик команды /start
@router.message(Command("start"))
async def start_command(message: types.Message):
    user_data[message.chat.id] = {}
    logger.info(f"Пользователь {message.from_user.id} начал сессию.")
    await message.answer("Привет! Я кулинарный бот. Напиши список ингредиентов через запятую:")

# Обработчик ввода ингредиентов
@router.message(lambda message: message.chat.id in user_data and "ingredients" not in user_data[message.chat.id])
async def handle_ingredients(message: types.Message):
    user_data[message.chat.id]["ingredients"] = message.text
    logger.info(f"Пользователь {message.from_user.id} ввёл ингредиенты: {message.text}")
    await message.answer("Введите страну мира, чью кухню хотите попробовать:")

# Обработчик ввода страны
@router.message(lambda message: message.chat.id in user_data and "country" not in user_data[message.chat.id])
async def handle_country(message: types.Message):
    user_data[message.chat.id]["country"] = message.text
    logger.info(f"Пользователь {message.from_user.id} выбрал страну: {message.text}")

    # Создание клавиатуры для выбора времени готовки
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text="Быстрое"))
    keyboard.add(KeyboardButton(text="Среднее"))
    keyboard.add(KeyboardButton(text="Долгое"))
    await message.answer("Выберите время готовки:", reply_markup=keyboard.as_markup(resize_keyboard=True))

# Обработчик выбора времени готовки
@router.message(lambda message: message.chat.id in user_data and "cooking_time" not in user_data[message.chat.id])
async def handle_cooking_time(message: types.Message):
    if message.text not in ["Быстрое", "Среднее", "Долгое"]:
        await message.answer("Пожалуйста, выберите время готовки из предложенных вариантов.")
        return

    user_data[message.chat.id]["cooking_time"] = message.text
    ingredients = user_data[message.chat.id]["ingredients"]
    country = user_data[message.chat.id]["country"]
    cooking_time = message.text.lower()

    # Вызов заглушки модели
    response = await mock_model_response(ingredients, country, cooking_time)
    logger.info(f"Пользователь {message.from_user.id} получил ответ: {response}")
    await message.answer(response, reply_markup=types.ReplyKeyboardRemove())

    # Очистка данных пользователя после ответа
    del user_data[message.chat.id]

# Запуск бота
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
