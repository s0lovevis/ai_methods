import logging
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import asyncio
from models.flan_t5.flan_t5_model import FlanT5LargeRecipeGenerator  # Генератор рецептов
from translator import Translator  # Переводчик

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен Telegram-бота
TELEGRAM_TOKEN = ""

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
router = Router()

# Инициализация модели и переводчика
generator = FlanT5LargeRecipeGenerator()
translator = Translator(source_lang="ru", target_lang="en")

# Хранилище данных пользователя
user_data = {}

# Клавиатура для выбора типа блюда
type_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Десерт"), KeyboardButton(text="Закуска"), KeyboardButton(text="Горячее")]
    ],
    resize_keyboard=True
)

# Обработчик команды /start
@router.message(Command("start"))
async def start_command(message: types.Message):
    user_data[message.chat.id] = {"step": "meal_type"}  # Устанавливаем текущий шаг
    await message.answer(
        "👋 Привет! Я бот для генерации рецептов. Я помогу вам придумать блюдо на основе ваших предпочтений."
    )
    await message.answer(
        "Какой тип блюда вы хотите приготовить?",
        reply_markup=type_keyboard
    )

# Обработчик выбора типа блюда
@router.message(lambda msg: user_data.get(msg.chat.id, {}).get("step") == "meal_type")
async def handle_meal_type(message: types.Message):
    user_data[message.chat.id]["type"] = message.text
    user_data[message.chat.id]["step"] = "cuisine"  # Переходим к следующему шагу
    await message.answer(
        "Теперь укажите кухню мира (например, Итальянская, Французская, Азиатская):",
        reply_markup=ReplyKeyboardRemove()
    )

# Обработчик выбора кухни
@router.message(lambda msg: user_data.get(msg.chat.id, {}).get("step") == "cuisine")
async def handle_cuisine(message: types.Message):
    user_data[message.chat.id]["cuisine"] = message.text
    user_data[message.chat.id]["step"] = "ingredients"  # Переходим к следующему шагу
    await message.answer("Перечислите ингредиенты через запятую:")

# Обработчик ввода ингредиентов
@router.message(lambda msg: user_data.get(msg.chat.id, {}).get("step") == "ingredients")
async def handle_ingredients(message: types.Message):
    user_data[message.chat.id]["ingredients"] = message.text
    user_data[message.chat.id]["step"] = "processing"  # Помечаем шаг как обработку

    # Сообщение о начале генерации
    await message.answer("🤖 Модель думает... Пожалуйста, подождите несколько секунд.")

    try:
        # Перевод пользовательского ввода на английский
        ingredients_en = translator.translate_to_en(user_data[message.chat.id]["ingredients"])
        type_en = translator.translate_to_en(user_data[message.chat.id]["type"])
        cuisine_en = translator.translate_to_en(user_data[message.chat.id]["cuisine"])

        # Создание промпта для модели
        prompt = f"Write a recipe for a {type_en} in {cuisine_en} style using the following ingredients: {ingredients_en}."

        # Генерация рецепта
        recipe_en = generator.generate(prompt)

        # Перевод рецепта обратно на русский
        recipe_ru = translator.translate_to_ru(recipe_en)

        # Отправка результата пользователю
        await message.answer(f"✨ Вот ваш рецепт:\n\n{recipe_ru}")
        await message.answer("Чтобы начать заново - отправьте любое сообщение.")

        # Очистка данных пользователя
        user_data.pop(message.chat.id, None)

    except Exception as e:
        logger.error(f"Ошибка при генерации рецепта: {e}")
        await message.answer("Произошла ошибка при генерации рецепта. Попробуйте снова позже.")

# Обработчик для сообщений "начать заново"
@router.message()
async def fallback_handler(message: types.Message):
    await start_command(message)

# Запуск бота
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
