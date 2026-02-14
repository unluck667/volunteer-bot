from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

TOKEN = "8599078171:AAH3AtojGltRrArQuLmSkh3LKa2DmaSbNMw"
ADMIN_ID = 123456789  # <-- сюда вставьте свой Telegram ID

# Главное меню
main_keyboard = ReplyKeyboardMarkup(
    [
        ["📋 Услуги", "ℹ О боте"],
        ["✍ Оставить заявку"]
    ],
    resize_keyboard=True
)

# Кнопка "Назад"
back_keyboard = ReplyKeyboardMarkup(
    [["⬅ Назад"]],
    resize_keyboard=True
)

# Команда старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте! Какая помощь вам понадобится?",
        reply_markup=main_keyboard
    )

# Обработка текста
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📋 Услуги":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💻 Разработка", callback_data="dev")],
            [InlineKeyboardButton("🎨 Дизайн", callback_data="design")]
        ])
        await update.message.reply_text("Выберите услугу:", reply_markup=keyboard)

    elif text == "ℹ О боте":
        await update.message.reply_text(
            "Я продвинутый Telegram-бот на Python 🤖",
            reply_markup=back_keyboard
        )

    elif text == "✍ Оставить заявку":
        await update.message.reply_text(
            "Опишите вашу задачу:",
            reply_markup=back_keyboard
        )
        context.user_data["waiting_for_request"] = True

    elif text == "⬅ Назад":
        context.user_data.clear()
        await update.message.reply_text(
            "Вы вернулись в главное меню 👇",
            reply_markup=main_keyboard
        )

    elif context.user_data.get("waiting_for_request"):
        # Отправляем заявку админу
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 Новая заявка:\n\nОт: {update.message.from_user.full_name}\n\n{text}"
        )
        await update.message.reply_text(
            "✅ Ваша заявка отправлена!",
            reply_markup=main_keyboard
        )
        context.user_data.clear()

    else:
        await update.message.reply_text(
            "Пожалуйста, используйте меню 👇",
            reply_markup=main_keyboard
        )

# Обработка inline-кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "dev":
        await query.edit_message_text("💻 Разработка ботов и сайтов.")
    elif query.data == "design":
        await query.edit_message_text("🎨 Дизайн интерфейсов и логотипов.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
