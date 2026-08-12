import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)


# =========================
# SETTINGS
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")

REGISTER_URL = "https://shorturl.at/gV00d"
SUPPORT_URL = "https://t.me/tayoacademy1"

PORT = int(os.getenv("PORT", "10000"))
RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Register on PO",
                url=REGISTER_URL
            )
        ],
        [
            InlineKeyboardButton(
                "✅ I've Registered",
                callback_data="registered"
            )
        ],
        [
            InlineKeyboardButton(
                "💬 Support ↗️",
                url=SUPPORT_URL
            )
        ],
    ]

    message = (
       message = (
    "🤖 *KU SOO DHAWOOW TAYO*\n\n"
    "Waxaan kuu qaban karaa:\n\n"
    "📊 Macluumaadka Trading-ka\n"
    "🎮 Habka Demo-ga\n"
    "📚 Casharro iyo Waxbarasho\n\n"
    "Si aad u bilowdo, samee akoonkaaga Pocket Option 👇"
)
    )

    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


# =========================
# I'VE REGISTERED
# =========================

async def registered(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    context.user_data["waiting_for_id"] = True

    await query.message.reply_text(
        "✅ *I've Registered*\n\n"
        "Please enter your Pocket Option ID 👇\n\n"
        "Example:\n"
        "`12345678`",
        parse_mode="Markdown"
    )


# =========================
# RECEIVE PO ID
# =========================

async def receive_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.user_data.get("waiting_for_id"):
        return

    po_id = update.message.text.strip()

    context.user_data["waiting_for_id"] = False
    context.user_data["po_id"] = po_id

    await update.message.reply_text(
        "🔎 *Pocket Option ID received.*\n\n"
        f"🆔 ID: `{po_id}`\n\n"
        "⏳ Your registration is being checked.\n\n"
        "⚠️ Registration will only be confirmed "
        "after official verification.",
        parse_mode="Markdown"
    )


# =========================
# MAIN
# =========================

def main():

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is missing.")

    if not RENDER_URL:
        raise ValueError("RENDER_EXTERNAL_URL is missing.")

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CallbackQueryHandler(
            registered,
            pattern="^registered$"
        )
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            receive_id
        )
    )

    webhook_url = f"{RENDER_URL}/telegram"

    print("Tayo Bot starting...")
    print(f"Webhook: {webhook_url}")

    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="telegram",
        webhook_url=webhook_url,
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
