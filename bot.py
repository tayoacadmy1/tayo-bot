import os
import logging

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ==============================
# SETTINGS
# ==============================

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_URL = "https://t.me/TokenFursadahaOnlineka"

# ==============================
# LOGGING
# ==============================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# ==============================
# /START
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    welcome_text = (
        "🤖 *KU SOO DHAWOW TAYO TRADING BOT!*\n\n"
        "Halkan waxaad ka heli kartaa:\n\n"
        "📊 Macluumaadka Trading-ka\n"
        "🎮 Habka Demo-ga\n"
        "📢 Channel-ka Tayo\n\n"
        "Dooro qaybta aad rabto 👇"
    )

keyboard = [
    [
        InlineKeyboardButton(
            "🚀 Iska Diiwaangeli Pocket Option",
            url="https://shorturl.at/gV00d"
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
            "💬 Taageero",
            url=SUPPORT_URL
        )
    ],
]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=reply_markup
    )


# ==============================
# TRADING INFO
# ==============================

async def trading_info(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    message = (
        "📊 *MACLUUMAADKA TRADING-KA*\n\n"
        "TAYO TRADING BOT wuxuu kaa caawinayaa "
        "inaad hesho macluumaad iyo faham ku saabsan trading-ka.\n\n"
        "📈 Fahamka suuqa\n"
        "📊 Akhrinta chart-ka\n"
        "🎯 Fahamka entry-ga\n"
        "⚠️ Maareynta khatarta\n\n"
        "📢 Wixii macluumaad dheeraad ah "
        "booqo Channel-ka Tayo."
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 Booqo Channel-ka",
                url=CHANNEL_URL
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Dib ugu noqo",
                callback_data="back_home"
            )
        ],
    ]

    await query.edit_message_text(
        message,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==============================
# DEMO
# ==============================

async def demo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    message = (
        "🎮 *HABKA DEMO-GA*\n\n"
        "Demo-ga waxaad ku baran kartaa trading-ka "
        "adigoon lacag dhab ah isticmaalin.\n\n"
        "Waxaad ku tababaran kartaa:\n"
        "📊 Akhrinta chart-ka\n"
        "🎯 Entry iyo Exit\n"
        "📈 Fahamka suuqa\n"
        "⚠️ Maareynta khatarta\n\n"
        "Markaad diyaar noqoto, waxaad sii baran kartaa "
        "trading-ka adigoo raacaya Tayo Academy."
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 Booqo Channel-ka",
                url=CHANNEL_URL
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Dib ugu noqo",
                callback_data="back_home"
            )
        ],
    ]

    await query.edit_message_text(
        message,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==============================
# BACK HOME
# ==============================

async def back_home(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    welcome_text = (
        "🤖 *KU SOO DHAWOW TAYO TRADING BOT!*\n\n"
        "Halkan waxaad ka heli kartaa:\n\n"
        "📊 Macluumaadka Trading-ka\n"
        "🎮 Habka Demo-ga\n"
        "📢 Channel-ka Tayo\n\n"
        "Dooro qaybta aad rabto 👇"
    )

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
                "📢 Booqo Channel-ka",
                url=CHANNEL_URL
            )
        ],
    ]

    await query.edit_message_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ==============================
# CALLBACK HANDLER
# ==============================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    if query.data == "trading_info":
        await trading_info(update, context)

    elif query.data == "demo":
        await demo(update, context)

    elif query.data == "back_home":
        await back_home(update, context)


# ==============================
# ERROR HANDLER
# ==============================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logger.error(
        "Exception while handling update:",
        exc_info=context.error
    )


# ==============================
# MAIN
# ==============================

# =========================
# MAIN
# =========================

def main():

    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN lama helin. Fadlan ka hubi Render Environment Variables."
        )

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # =========================
    # START COMMAND
    # =========================

    application.add_handler(
        CommandHandler("start", start)
    )

    # =========================
    # BUTTONS
    # =========================

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    # =========================
    # ERROR HANDLER
    # =========================

    application.add_error_handler(error_handler)

    # =========================
    # RENDER WEBHOOK
    # =========================

    port = int(os.getenv("PORT", "10000"))
    render_url = os.getenv("RENDER_EXTERNAL_URL")

    if not render_url:
        raise ValueError(
            "RENDER_EXTERNAL_URL lama helin. "
            "Hubi Render Environment Variables."
        )

    webhook_url = f"{render_url}/telegram"

    print("🤖 TAYO TRADING BOT waa bilaabanayaa...")
    print(f"🌐 Webhook URL: {webhook_url}")
    print(f"🔌 Port: {port}")

    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path="telegram",
        webhook_url=webhook_url,
        drop_pending_updates=True
    )


# =========================
# RUN
# =========================

if __name__ == "__main__":
    main()
