import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
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

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

keyboard = [
    [
        InlineKeyboardButton(
            "📊 Macluumaadka Trading-ka",
            callback_data="trading_info"
        )
    ],
    [
        InlineKeyboardButton(
            "🎮 Habka Demo-ga",
            callback_data="demo"
        )
    ],
    [
        InlineKeyboardButton(
            "📚 Casharro iyo Waxbarasho",
            callback_data="lessons"
        )
    ],
    [
        InlineKeyboardButton(
            "📢 Booqo Channel-ka",
            url="https://t.me/TokenFursadahaOnlineka"
        )
    ],
    [
        InlineKeyboardButton(
            "💬 Taageero ↗️",
            url=SUPPORT_URL
        )
    ],
]

    message = (
        "🤖 *KU SOO DHAWOW TAYO*\n\n"
        "Waxaan kuu qaban karaa:\n\n"
        "📊 Macluumaadka Trading-ka\n"
        "🎮 Habka Demo-ga\n"
        "📚 Casharro iyo Waxbarasho\n\n"
        "Si aad u bilowdo, samee akoonkaaga Pocket Option 👇"
    )

    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


# =========================
# I'VE REGISTERED
# =========================

async def registered(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "✅ *Waan helnay.*\n\n"
        "Fadlan geli Pocket Option ID-gaaga 👇\n\n"
        "Tusaale:\n"
        "`12345678`",
        parse_mode="Markdown"
    )

    context.user_data["waiting_for_id"] = True


# =========================
# RECEIVE POCKET OPTION ID
# =========================

async def receive_id(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not context.user_data.get("waiting_for_id"):
        return

    user_id = update.message.text.strip()

    if not user_id.isdigit():
        await update.message.reply_text(
            "⚠️ Fadlan geli Pocket Option ID sax ah.\n\n"
            "Tusaale: `12345678`",
            parse_mode="Markdown"
        )
        return

    context.user_data["waiting_for_id"] = False

    await update.message.reply_text(
        "🔎 *Pocket Option ID waa la helay.*\n\n"
        f"🆔 ID: `{user_id}`\n\n"
        "⏳ Diiwaangelintaada waa la hubinayaa.\n\n"
        "⚠️ Xaqiijinta waxaa la sameyn doonaa kadib "
        "hubin rasmi ah.",
        parse_mode="Markdown"
    )


# =========================
# MAIN
# =========================

def main():

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN lama helin.")

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

    if not RENDER_URL:
        raise ValueError(
            "RENDER_EXTERNAL_URL lama helin."
        )

    webhook_url = f"{RENDER_URL}/telegram"

    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="telegram",
        webhook_url=webhook_url,
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
