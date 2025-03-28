# import logging
#
# from telegram import Update
# from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
#
# # Enable logging
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )
# logger = logging.getLogger(__name__)
#
#
# # Обработчик команды /start
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот.")
#
#
# if __name__ == '__main__':
#     # Замените 'YOUR_TELEGRAM_BOT_TOKEN' на ваш токен бота
#     application = ApplicationBuilder().token('').build()
#
#     # Добавление обработчика команды /start
#     start_handler = CommandHandler('start', start)
#     application.add_handler(start_handler)
#
#     # Запуск бота
#     application.run_polling()


# import logging
# from telegram import Update
# from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
#
# # Включить логирование
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )
# logger = logging.getLogger(__name__)
#
# # --- Обработчики команд ---
#
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Обработчик команды /start."""
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот. Используйте /help, чтобы узнать, что я умею.")
#
# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Обработчик команды /help."""
#     help_text = """
#     Я бот, который умеет делать следующее:
#
#     /start - Начать общение с ботом
#     /help - Показать это сообщение
#     /caps <text> - Преобразовать текст в верхний регистр
#     /echo <text> - Повторить введенный текст
#     """
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)
#
#
# async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Обработчик команды /caps."""
#     if context.args:  # Проверяем, есть ли аргументы у команды
#         text_caps = ' '.join(context.args).upper() # Преобразуем аргументы в верхний регистр
#         await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
#     else:
#         await context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, введите текст после команды /caps.")
#
# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Обработчик команды /echo."""
#     if context.args:
#         text = ' '.join(context.args)
#         await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
#     else:
#         await context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, введите текст после команды /echo.")
#
#
#
# # --- Обработчик ошибок ---
# async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Log the error and send a telegram message to notify the developer."""
#     # Log the error before sending the message, so you can see what happened
#     logger.error(f"Update {update} caused error {context.error}")
#
#     # Optionally, send the error to the developer.
#     await update.message.reply_text(f"Произошла ошибка: {context.error}")
#
#
#
# if __name__ == '__main__':
#     # Замените 'YOUR_TELEGRAM_BOT_TOKEN' на ваш токен бота
#     application = ApplicationBuilder().token('7734145770:AAHM1aL6k_k7mHqZCt6yVEqAAVmFXTGTsDQ').build()
#
#     # --- Добавление обработчиков команд ---
#     application.add_handler(CommandHandler('start', start))
#     application.add_handler(CommandHandler('help', help_command))
#     application.add_handler(CommandHandler('caps', caps))
#     application.add_handler(CommandHandler('echo', echo))
#     application.add_error_handler(error_handler)
#
#
#     # --- Запуск бота ---
#     application.run_polling()

import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Стадии диалога
NAME, AGE = range(2)  # Создаем переменные для каждой стадии


# Функции-обработчики

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start."""
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Привет! Я бот для регистрации.  Введите команду /register чтобы начать.")
    return ConversationHandler.END  # Завершаем диалог /start


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало регистрации, запрашиваем имя."""
    await update.message.reply_text("Как вас зовут?")
    return NAME  # Переходим к стадии NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик для получения имени."""
    context.user_data['name'] = update.message.text
    await update.message.reply_text(f"Приятно познакомиться, {context.user_data['name']}!  Сколько вам лет?")
    return AGE  # Переходим к стадии AGE


async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик для получения возраста."""
    try:
        age = int(update.message.text)
        context.user_data['age'] = age
        await update.message.reply_text(
            f"Отлично!  Ваше имя: {context.user_data['name']}, возраст: {context.user_data['age']}.  Регистрация завершена.")
        #  Здесь можно сохранить данные в базу данных или выполнить другие действия
        return ConversationHandler.END  # Завершаем диалог
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число (возраст).")
        return AGE  # Остаемся на стадии AGE, т.к. ввод неверный


async def lastName(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик для получения Фамилии."""
    context.user_data['laastname'] = update.message.text
    await update.message.reply_text(
        f"Укажите свою фамилию или как бы Вы хотели к Вам обращаться, {context.user_data['lastname']}! ")
    # return AGE  # Переходим к стадии AGE


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /cancel (отмена регистрации)."""
    await update.message.reply_text("Регистрация отменена.")
    return ConversationHandler.END


# --- Обработчик ошибок ---
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before sending the message, so you can see what happened
    logger.error(f"Update {update} caused error {context.error}")
    await update.message.reply_text(f"Произошла ошибка: {context.error}")


if __name__ == '__main__':
    # Замените 'YOUR_TELEGRAM_BOT_TOKEN' на ваш токен бота
    application = ApplicationBuilder().token('7734145770:AAHM1aL6k_k7mHqZCt6yVEqAAVmFXTGTsDQ').build()

    # --- ConversationHandler ---
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('register', register)],  # Точка входа (команда /register)
        states={  # Определяем стадии и обработчики для каждой стадии
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],  # Обрабатываем ввод имени
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age)],  # Обрабатываем ввод возраста
            lastName: [MessageHandler(filters.TEXT & ~filters.COMMAND, lastName)],  # Обра��атываем ввод фамилии (не используется в данном примере)
        },
        fallbacks=[CommandHandler('cancel', cancel)],  # Обработчик для команды /cancel (отмена)
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('start', start))
    application.add_error_handler(error_handler)

    # --- Запуск бота ---
    application.run_polling()
