from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8004644159:AAHpTPScjFTiI45zG7uUbJh4q41xNrLupXU"  # Лучше передавать через переменную окружения
ADMIN_ID = 1267693167  # Твой Telegram ID для получения вопросов

# Кнопки и тексты для них
buttons = [
    ["ℹ️ Обо мне", "📝 Записаться на пробное"],
    ["💳 Абонементы", "🎓 Я репетитор, хочу курс"],
    ["❓ Задать вопрос"]
]

messages = {
    "ℹ️ Обо мне": "📚 Подробнее обо мне: https://daria-emelianova.yonote.ru/share/rus",
    "📝 Записаться на пробное": "📝 Анкета на пробное: https://forms.yandex.ru/u/683ad41feb61464bc78c1b3e",
    "💳 Абонементы": "💳 Абонементы: https://daria-emelianova.yonote.ru/share/abonement",
    "🎓 Я репетитор, хочу курс": "🎓 Курс для репетиторов: https://daria-emelianova.yonote.ru/share/kabinet"
}

# Словарь для хранения состояния "задаёт вопрос"
user_question_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(
        "Я бот Дарьи Емельяновой. Чем могу помочь?",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if text == "❓ Задать вопрос":
        user_question_state[user_id] = True
        await update.message.reply_text("Задавайте вопрос прямо здесь, я передам его Дарье.")
        return

    if user_question_state.get(user_id, False):
        user_info = update.message.from_user
        username = user_info.username or user_info.first_name
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"Вопрос от @{username} ({user_info.first_name}): {text}"
        )
        await update.message.reply_text("Спасибо за вопрос! Я передам его Дарье.")
        user_question_state[user_id] = False
        return

    if text in messages:
        await update.message.reply_text(messages[text])
    else:
        await update.message.reply_text("Пожалуйста, выбери кнопку из меню.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
