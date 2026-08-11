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

# Halkan dambe waxaan gelin doonaa Pocket Option referral link-gaaga
REGISTER_URL = "https://pocketoption.com/en/register/"

# Support-kaaga Telegram
SUPPORT_URL = "https://t.me/tayoacadmy1"


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

    reply_markup = InlineKeyboardMarkup(keyboard)

    message = (
        "🤖 *WELCOME TO TAYO*\n\n"
        "What I can do:\n\n"
        "📊 Trading Information\n"
        "🎮 Demo Mode\n"
        "📚 Educational Content\n\n"
        "To get started, create your Pocket Option account 👇"
    )

    await update.message.reply_text(
        message,
        reply_markup=reply_markup,
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
        "⚠️ Verification will only be confirmed when an official "
        "verification method is available.",
        parse_mode="Markdown"
    )


# =========================
# MAIN
# =========================

def main():

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set.")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        CallbackQueryHandler(
            registered,
            pattern="^registered$"
        )
    )
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            receive_id
        )
    )

    print("Tayo Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
