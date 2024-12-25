import logging
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен Telegram-бота
TELEGRAM_TOKEN = "7604679620:AAFb9Gs3wCca1PEcLMF4j8ENfNaqbfhgddQ"

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
router = Router()

# Хранилище данных пользователя
user_data = {}

# Клавиатуры
model_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="GPT2 fine-tuned"), KeyboardButton(text="T-Lite instruct")],
        [KeyboardButton(text="Расскажи подробнее про модели")]
    ],
    resize_keyboard=True
)

back_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Понятно")]],
    resize_keyboard=True
)

post_recipe_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Хочу еще рецепт!"), KeyboardButton(text="Закончить работу")]
    ],
    resize_keyboard=True
)

# Обработчик команды /start
@router.message(Command("start"))
async def start_command(message: types.Message):
    user_data[message.chat.id] = {"step": "choose_model"}
    await message.answer(
        "👋 Привет! Я бот для генерации рецептов. Я помогу вам придумать блюдо на основе ваших предпочтений."
    )
    await message.answer(
        "Выбери нейросетевую модель, которая будет генерировать рецепт:",
        reply_markup=model_keyboard
    )

# Обработчик выбора модели
@router.message(lambda msg: user_data.get(msg.chat.id, {}).get("step") == "choose_model")
async def choose_model(message: types.Message):
    if message.text == "Расскажи подробнее про модели":
        user_data[message.chat.id]["step"] = "model_info"
        await message.answer(
            "GPT2 fine-tuned - специализированная модель для генерации рецептов.\n"
            "T-Lite instruct - новая модель, находится в разработке.",
            reply_markup=back_keyboard
        )
    elif message.text in ["GPT2 fine-tuned", "T-Lite instruct"]:
        if message.text == "T-Lite instruct":
            await message.answer(
                "Данная модель в разработке, выбери другую.",
                reply_markup=model_keyboard
            )
        else:
            user_data[message.chat.id]["model"] = message.text
            user_data[message.chat.id]["step"] = "input_ingredients"
            await message.answer(
                "Отлично! Введите ингредиенты через запятую:",
                reply_markup=ReplyKeyboardRemove()
            )
    else:
        await message.answer("Пожалуйста, выберите доступный вариант.", reply_markup=model_keyboard)

# Обработчик информации о моделях
@router.message(lambda msg: user_data.get(msg.chat.id, {}).get("step") == "model_info")
async def model_info(message: types.Message):
    if message.text == "Понятно":
        user_data[message.chat.id]["step"] = "choose_model"
        await message.answer(
            "Выбери нейросетевую модель, которая будет генерировать рецепт:",
            reply_markup=model_keyboard
        )
    else:
        await message.answer("Нажмите 'Понятно', чтобы вернуться к выбору модели.")

# Обработчик ввода ингредиентов
@router.message(lambda msg: user_data.get(msg.chat.id, {}).get("step") == "input_ingredients")
async def input_ingredients(message: types.Message):
    user_data[message.chat.id]["ingredients"] = message.text
    user_data[message.chat.id]["step"] = "generate_recipe"
    await message.answer("🤖 Модель думает... Пожалуйста, подождите 15-20 секунд.")

    # Здесь нужно подключить логику генерации рецепта
    # Пока просто заглушка
    await asyncio.sleep(5)  # Имитация работы модели
    recipe = "Ваш рецепт: смешайте все ингредиенты и подавайте!"  # Заглушка

    await message.answer(recipe)
    await message.answer(
        "Что вы хотите сделать дальше?",
        reply_markup=post_recipe_keyboard
    )

# Обработчик действий после выдачи рецепта
@router.message(lambda msg: user_data.get(msg.chat.id, {}).get("step") == "generate_recipe")
async def post_recipe_action(message: types.Message):
    if message.text == "Хочу еще рецепт!":
        user_data[message.chat.id]["step"] = "choose_model"
        await message.answer(
            "Выбери нейросетевую модель, которая будет генерировать рецепт:",
            reply_markup=model_keyboard
        )
    elif message.text == "Закончить работу":
        await message.answer(
            "Всего доброго! Чтобы начать заново, отправьте /start.",
            reply_markup=ReplyKeyboardRemove()
        )
        user_data.pop(message.chat.id, None)
    else:
        await message.answer(
            "Пожалуйста, выберите один из доступных вариантов:",
            reply_markup=post_recipe_keyboard
        )

# Запуск бота
async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
