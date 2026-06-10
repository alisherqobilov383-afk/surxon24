import sys
import asyncio
import os

# --- 1. Loopni eng birinchi bo'lib sozlaymiz ---
if sys.platform != 'win32':
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass

# Loopni yaratib, joriy thread uchun o'rnatamiz
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# --- 2. Endi boshqa kutubxonalarni import qilamiz ---
from flask import Flask
from threading import Thread
from pyrogram import Client, filters

# --- SERVER ---
flask_app = Flask("")
@flask_app.route("/")
def home(): return "Bot 24/7 ishlamoqda!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

Thread(target=run_flask, daemon=True).start()

# --- SOZLAMALAR ---
CONFIG = {
    "surxondaryo_rasmiy": {
        "target": "surxon_24_live",
        "replacements": {
            "Сурхондарёдаги тезкор янгиликлар каналига обуна бўлинг": "https://t.me/surxon_24_live"
        }
    }
}

async def start_bot():
    app = Client(
        "render_userbot", 
        api_id=int(os.environ.get("API_ID")), 
        api_hash=os.environ.get("API_HASH"), 
        session_string=os.environ.get("SESSION_STRING")
    )

    @app.on_message(filters.chat(list(CONFIG.keys())))
    async def handler(client, message):
        chat_username = message.chat.username
        conf = CONFIG.get(chat_username)
        if not conf: return

        text = message.caption or message.text or ""
        new_text = text
        for old, new in conf["replacements"].items():
            new_text = new_text.replace(old, new)
        
        try:
            await client.copy_message(
                chat_id=conf["target"],
                from_chat_id=message.chat.id,
                message_id=message.id,
                caption=new_text[:1024]
            )
            print(f"✅ {chat_username} ga yuborildi.")
        except Exception as e:
            print(f"❌ Xatolik: {e}")

    await app.start()
    print("🚀 Bot ishga tushdi!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop.run_until_complete(start_bot())
