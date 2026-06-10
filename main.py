import sys
import os
import asyncio

# --- MUHIM: Python 3.14 va Render uchun loopni oldindan sozlash ---
if sys.platform != 'win32':
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        # Agar uvloop bo'lmasa, standart loopni o'rnatamiz
        asyncio.set_event_loop(asyncio.new_event_loop())
else:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Endi qolgan kutubxonalarni import qilamiz
from flask import Flask
from threading import Thread
from pyrogram import Client, filters

# --- SERVER (24/7 ishlashi uchun) ---
flask_app = Flask("")
@flask_app.route("/")
def home(): return "Bot 24/7 ishlamoqda!"

def run_flask():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

Thread(target=run_flask, daemon=True).start()

# --- SOZLAMALAR ---
CONFIG = {
    "SurxondaryoRasmiy": {
        "target": "surxon_24_live",
        "replacements": {
            "Сурхондарёдаги тезкор янгиликлар каналига обуна бўлинг": "https://t.me/surxon_24_live",
            "MEqqwqwqwDIA": "https://t.me/eltua",
            "qwqwqwqw": "https://x.com/eltz"
        }
    },
    "https://t.me/tuztuzttt": {
        "target": "https://t.me/surxon_24_live",
        "replacements": {
            "Surxondaryoning eng aktiv kanali👇": "https://t.me/surxon_24_live",
            "Facebook": "https://www.facebook.com/profile.php?id=61585wqqwd818251235"
        }
    }
}

async def start_bot():
    # Client ni yaratamiz
    app = Client(
        "render_userbot", 
        api_id=int(os.environ.get("API_ID")), 
        api_hash=os.environ.get("API_HASH"), 
        session_string=os.environ.get("SESSION_STRING")
    )

    @app.on_message(filters.chat(list(CONFIG.keys())))
    async def handler(client, message):
        chat_username = f"@{message.chat.username}"
        conf = CONFIG.get(chat_username)
        
        text = message.caption or message.text or ""
        
        new_text = text
        for old_word, new_link in conf["replacements"].items():
            new_text = new_text.replace(old_word, new_link)
        
        try:
            await client.copy_message(
                chat_id=conf["target"],
                from_chat_id=message.chat.id,
                message_id=message.id,
                caption=new_text
            )
            print(f"✅ {chat_username} -> {conf['target']} muvaffaqiyatli!")
        except Exception as e:
            print(f"❌ Xatolik ({chat_username}): {e}")

    await app.start()
    print("🚀 Bot ko'p kanalli rejimda ishga tushdi!")
    # Event loopni to'xtatmasdan ushlab turamiz
    await asyncio.Event().wait()

if __name__ == "__main__":
    # Python 3.14 da eng barqaror ishlaydigan usul
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
