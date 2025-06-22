import logging
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from sheets_manager import SheetsManager
from validators import validate_phone, validate_email
from bot_states import UserStates

# Получаем токен бота из переменных окружения
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Глобальные переменные для состояний пользователей
user_states = {}
user_data = {}

# Инициализация менеджера Google Sheets
sheets_manager = SheetsManager()

def get_main_keyboard():
    """Создает основную клавиатуру с кнопкой для добавления записи"""
    keyboard = [
        [KeyboardButton("➕ Добавить запись")],
        [KeyboardButton("📋 Показать данные"), KeyboardButton("🔄 Очистить")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def get_cancel_keyboard():
    """Создает клавиатуру с кнопками отмены и пропуска"""
    keyboard = [
        [KeyboardButton("⏭️ Пропустить"), KeyboardButton("❌ Отмена")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user_id = update.effective_user.id
    user_states[user_id] = UserStates.MAIN_MENU
    user_data[user_id] = {"phone": "", "email": "", "name": "", "type": ""}
    
    welcome_message = (
        "🤖 Добро пожаловать в бот для управления Google Sheets!\n\n"
        "Нажмите '➕ Добавить запись' чтобы начать заполнение данных.\n"
        "Бот последовательно запросит:\n"
        "1️⃣ Телефон\n"
        "2️⃣ Email\n" 
        "3️⃣ Имя\n"
        "4️⃣ Тайп\n\n"
        "После заполнения всех полей данные автоматически сохранятся в таблицу."
    )
    
    await update.message.reply_text(
        welcome_message,
        reply_markup=get_main_keyboard()
    )

async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик основного меню"""
    user_id = update.effective_user.id
    text = update.message.text
    
    if text == "➕ Добавить запись":
        # Очищаем данные и начинаем новую запись
        user_data[user_id] = {"phone": "", "email": "", "name": "", "type": ""}
        user_states[user_id] = UserStates.WAITING_PHONE
        await update.message.reply_text(
            "1️⃣ Введите номер телефона (например: +7 999 123-45-67)\nили нажмите 'Пропустить' чтобы оставить поле пустым:",
            reply_markup=get_cancel_keyboard()
        )
    
    elif text == "📋 Показать данные":
        await show_current_data(update, context)
    
    elif text == "🔄 Очистить":
        user_data[user_id] = {"phone": "", "email": "", "name": "", "type": ""}
        await update.message.reply_text(
            "🔄 Данные очищены!",
            reply_markup=get_main_keyboard()
        )
    
    else:
        await show_current_data(update, context)

async def handle_phone_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ввода телефона"""
    user_id = update.effective_user.id
    text = update.message.text
    
    if text == "❌ Отмена":
        user_states[user_id] = UserStates.MAIN_MENU
        await update.message.reply_text(
            "Ввод телефона отменен.",
            reply_markup=get_main_keyboard()
        )
        return
    
    if text == "⏭️ Пропустить":
        user_data[user_id]["phone"] = ""
        user_states[user_id] = UserStates.WAITING_EMAIL
        await update.message.reply_text(
            "⏭️ Телефон пропущен\n\n2️⃣ Теперь введите адрес электронной почты\nили нажмите 'Пропустить':",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    if validate_phone(text):
        user_data[user_id]["phone"] = text
        user_states[user_id] = UserStates.WAITING_EMAIL
        await update.message.reply_text(
            f"✅ Телефон сохранен: {text}\n\n2️⃣ Теперь введите адрес электронной почты\nили нажмите 'Пропустить':",
            reply_markup=get_cancel_keyboard()
        )
    else:
        await update.message.reply_text(
            "❌ Неверный формат телефона. Введите номер в формате +7 999 123-45-67:",
            reply_markup=get_cancel_keyboard()
        )

async def handle_email_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ввода email"""
    user_id = update.effective_user.id
    text = update.message.text
    
    if text == "❌ Отмена":
        user_states[user_id] = UserStates.MAIN_MENU
        await update.message.reply_text(
            "Ввод email отменен.",
            reply_markup=get_main_keyboard()
        )
        return
    
    if text == "⏭️ Пропустить":
        user_data[user_id]["email"] = ""
        user_states[user_id] = UserStates.WAITING_NAME
        await update.message.reply_text(
            "⏭️ Email пропущен\n\n3️⃣ Теперь введите имя\nили нажмите 'Пропустить':",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    if validate_email(text):
        user_data[user_id]["email"] = text
        user_states[user_id] = UserStates.WAITING_NAME
        await update.message.reply_text(
            f"✅ Email сохранен: {text}\n\n3️⃣ Теперь введите имя\nили нажмите 'Пропустить':",
            reply_markup=get_cancel_keyboard()
        )
    else:
        await update.message.reply_text(
            "❌ Неверный формат email. Введите корректный адрес электронной почты:",
            reply_markup=get_cancel_keyboard()
        )

async def handle_name_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ввода имени"""
    user_id = update.effective_user.id
    text = update.message.text
    
    if text == "❌ Отмена":
        user_states[user_id] = UserStates.MAIN_MENU
        await update.message.reply_text(
            "Ввод имени отменен.",
            reply_markup=get_main_keyboard()
        )
        return
    
    if text == "⏭️ Пропустить":
        user_data[user_id]["name"] = ""
        user_states[user_id] = UserStates.WAITING_TYPE
        await update.message.reply_text(
            "⏭️ Имя пропущено\n\n4️⃣ Наконец, введите тип\nили нажмите 'Пропустить':",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    if text.strip():
        user_data[user_id]["name"] = text.strip()
        user_states[user_id] = UserStates.WAITING_TYPE
        await update.message.reply_text(
            f"✅ Имя сохранено: {text.strip()}\n\n4️⃣ Наконец, введите тип\nили нажмите 'Пропустить':",
            reply_markup=get_cancel_keyboard()
        )
    else:
        await update.message.reply_text(
            "❌ Имя не может быть пустым. Введите имя или нажмите 'Пропустить':",
            reply_markup=get_cancel_keyboard()
        )

async def handle_type_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ввода типа"""
    user_id = update.effective_user.id
    text = update.message.text
    
    if text == "❌ Отмена":
        user_states[user_id] = UserStates.MAIN_MENU
        await update.message.reply_text(
            "Ввод типа отменен.",
            reply_markup=get_main_keyboard()
        )
        return
    
    if text == "⏭️ Пропустить":
        user_data[user_id]["type"] = ""
        # Автоматически сохраняем данные после пропуска последнего поля
        await save_data(update, context)
        return
    
    if text.strip():
        user_data[user_id]["type"] = text.strip()
        # Автоматически сохраняем данные после ввода последнего поля
        await save_data(update, context)
    else:
        await update.message.reply_text(
            "❌ Тип не может быть пустым. Введите тип или нажмите 'Пропустить':",
            reply_markup=get_cancel_keyboard()
        )

async def show_current_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает текущие введенные данные"""
    user_id = update.effective_user.id
    data = user_data.get(user_id, {"phone": "", "email": "", "name": "", "type": ""})
    
    status_message = "📋 Текущие данные:\n\n"
    status_message += f"📱 Телефон: {data['phone'] or '❌ Не заполнено'}\n"
    status_message += f"📧 Email: {data['email'] or '❌ Не заполнено'}\n"
    status_message += f"👤 Имя: {data['name'] or '❌ Не заполнено'}\n"
    status_message += f"🏷️ Тип: {data['type'] or '❌ Не заполнено'}\n\n"
    status_message += "Выберите столбец для заполнения или сохраните данные."
    
    await update.message.reply_text(
        status_message,
        reply_markup=get_main_keyboard()
    )

async def save_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Сохраняет данные в Google Sheets"""
    user_id = update.effective_user.id
    data = user_data.get(user_id, {"phone": "", "email": "", "name": "", "type": ""})
    
    try:
        # Сохраняем данные в Google Sheets
        success = sheets_manager.add_row([data["phone"], data["email"], data["name"], data["type"]])
        
        if success:
            user_states[user_id] = UserStates.MAIN_MENU
            await update.message.reply_text(
                "✅ Запись успешно добавлена в Google Sheets!\n\n"
                f"Телефон: {data['phone']}\n"
                f"Email: {data['email']}\n"
                f"Имя: {data['name']}\n"
                f"Тип: {data['type']}\n\n"
                "Нажмите '➕ Добавить запись' для новой записи.",
                reply_markup=get_main_keyboard()
            )
            # Очищаем данные после успешного сохранения
            user_data[user_id] = {"phone": "", "email": "", "name": "", "type": ""}
        else:
            user_states[user_id] = UserStates.MAIN_MENU
            await update.message.reply_text(
                "❌ Ошибка при сохранении данных в Google Sheets. Попробуйте позже.",
                reply_markup=get_main_keyboard()
            )
    
    except Exception as e:
        logger.error(f"Ошибка при сохранении данных: {e}")
        user_states[user_id] = UserStates.MAIN_MENU
        await update.message.reply_text(
            "❌ Произошла ошибка при сохранении данных. Попробуйте позже.",
            reply_markup=get_main_keyboard()
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Основной обработчик сообщений"""
    user_id = update.effective_user.id
    
    # Инициализируем пользователя, если его нет в состояниях
    if user_id not in user_states:
        user_states[user_id] = UserStates.MAIN_MENU
        user_data[user_id] = {"phone": "", "email": "", "name": "", "type": ""}
    
    current_state = user_states[user_id]
    
    if current_state == UserStates.MAIN_MENU:
        await handle_main_menu(update, context)
    elif current_state == UserStates.WAITING_PHONE:
        await handle_phone_input(update, context)
    elif current_state == UserStates.WAITING_EMAIL:
        await handle_email_input(update, context)
    elif current_state == UserStates.WAITING_NAME:
        await handle_name_input(update, context)
    elif current_state == UserStates.WAITING_TYPE:
        await handle_type_input(update, context)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Произошла ошибка: {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Произошла ошибка. Попробуйте /start для перезапуска бота.",
            reply_markup=get_main_keyboard()
        )

def main() -> None:
    """Основная функция запуска бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Запускаем бота
    logger.info("Запуск Telegram бота...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
