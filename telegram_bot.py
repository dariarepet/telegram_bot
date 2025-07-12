
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("TOKEN")  # Получаем токен из переменной окружения

keyboard = [
    ["ℹ️ Обо мне", "📝 Записаться на пробное"],
    ["💳 Абонементы", "🎓 Я репетитор, хочу курс"],
    ["❓ Задать вопрос"],
]

messages = {
    "ℹ️ Обо мне": "📚 Подробнее обо мне: https://daria-emelianova.yonote.ru/share/rus",
    "📝 Записаться на пробное": "📝 Анкета на пробное: https://forms.yandex.ru/u/683ad41feb61464bc78c1b3e",
    "💳 Абонементы": "💳 Абонементы: https://daria-emelianova.yonote.ru/share/abonement",
    "🎓 Я репетитор, хочу курс": "🎓 Курс для репетиторов: https://daria-emelianova.yonote.ru/share/kurs",
}

ADMIN_ID = 1267693167  # <-- твой Telegram ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Я бот Дарьи Емельяновой. Чем могу помочь?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in messages:
        await update.message.reply_text(messages[text])
    else:
        if text not in sum(keyboard, []):
            # Перешлём вопрос администратору
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"Вопрос от {update.message.from_user.first_name}: {text}")
            await update.message.reply_text("Спасибо за вопрос! Я передам его Дарье.")
        else:
            await update.message.reply_text("Пожалуйста, выбери кнопку из меню.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
