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

import os
TOKEN = os.getenv("TOKEN")
ADMIN_ID = 1519672570

# Главное меню
main_keyboard = ReplyKeyboardMarkup(
    [
        ["ℹ О боте"],
        ["📦 Заказать услугу"],
        ["🛠 Тех.поддержка"]
    ],
    resize_keyboard=True
)

back_keyboard = ReplyKeyboardMarkup(
    [["⬅ Назад"]],
    resize_keyboard=True
)

# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте! Какая помощь вам понадобится?",
        reply_markup=main_keyboard
    )

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user

    if text == "ℹ О боте":
        await update.message.reply_text(
            "Данный бот создан для помощи волонтёров людям в пожилом возрасте.",
            reply_markup=back_keyboard
        )

    elif text == "📦 Заказать услугу":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🤝 Совместный досуг", callback_data="service_Совместный досуг")],
            [InlineKeyboardButton("🚶 Прогулка", callback_data="service_Прогулка")],
            [InlineKeyboardButton("🏥 Сопровождение в поликлинику", callback_data="service_Поликлиника")],
            [InlineKeyboardButton("🏠 Бытовая помощь", callback_data="service_Бытовая помощь")],
            [InlineKeyboardButton("📱 Смартфон с нуля", callback_data="service_Смартфон")],
            [InlineKeyboardButton("✏ Другое", callback_data="service_Другое")]
        ])
        await update.message.reply_text("Выберите услугу:", reply_markup=keyboard)

    elif text == "🛠 Тех.поддержка":
        username = f"@{user.username}" if user.username else "без username"

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"🛠 Запрос в техподдержку\n\n"
                f"Пользователь: {username}\n"
                f"ID: {user.id}\n\n"
                f"Напишите этому человеку по вопросам техподдержки."
            )
        )

        await update.message.reply_text(
            "Запрос в техподдержку отправлен ✅",
            reply_markup=main_keyboard
        )

    elif text == "⬅ Назад":
        context.user_data.clear()
        await update.message.reply_text(
            "Главное меню 👇",
            reply_markup=main_keyboard
        )

    elif context.user_data.get("waiting_other"):
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"📨 Новый запрос (Другое)\n\n"
                f"От: {user.full_name}\n"
                f"ID: {user.id}\n\n"
                f"Описание:\n{text}"
            )
        )

        await update.message.reply_text(
            "Отлично, с вами скоро свяжутся.\nЗапрос отправлен ✅",
            reply_markup=main_keyboard
        )

        context.user_data.clear()

    else:
        await update.message.reply_text("Пожалуйста, используйте меню 👇")

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user
    data = query.data

    if data.startswith("service_"):
        service_name = data.replace("service_", "")

        if service_name == "Другое":
            context.user_data["waiting_other"] = True
            await query.edit_message_text("Опишите, какая помощь вам требуется:")
        else:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=(
                    f"📨 Новый запрос на помощь\n\n"
                    f"От: {user.full_name}\n"
                    f"ID: {user.id}\n\n"
                    f"Услуга: {service_name}"
                )
            )

            await query.edit_message_text(
                "Отлично, с вами скоро свяжутся.\nЗапрос отправлен ✅"
            )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
