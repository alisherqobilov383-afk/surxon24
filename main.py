import sys
import os
import asyncio

# --- MUHIM: Python 3.14 va Render uchun loopni oldindan sozlash ---
if sys.platform != 'win32':
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        asyncio.set_event_loop(asyncio.new_event_loop())
else:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

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

# --- SOZLAMALAR (Kanal ID raqamlari bilan) ---
# Manbalar:
# SurxondaryoRasmiy: -1003797840044
# Termiz_yangiliklari: -1002123389775
# Target: -1003951220619

CONFIG = {
    -1001408261787: {
        "target": -1003951220619,
        "replacements": {
            "Сурхондарёдаги тезкор янгиликлар каналига обуна бўлинг": "https://t.me/surxon_24_live",
            "MEqqwqwqwDIA": "https://t.me/eltua",
            "qwqwqwqw": "https://x.com/eltz"
        }
    },
    -1002123389775: {
        "target": -1003951220619,
        "replacements": {
            "Surxondaryoning eng aktiv kanali👇": "https://t.me/surxon_24_live",
            "Facebook": "https://www.facebook.com/profile.php?id=61585818251235"
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

    await app.start()
    print("🚀 Bot muvaffaqiyatli ishga tushdi!")

    # Kanallarni keshga olish (resolve)
    for cid in CONFIG.keys():
        try:
            await app.get_chat(cid)
        except Exception:
            pass

    @app.on_message(filters.chat(list(CONFIG.keys())))
    async def handler(client, message):
        chat_id = message.chat.id
        conf = CONFIG.get(chat_id)
        
        text = message.caption or message.text or ""
        
        new_text = text
        for old_word, new_link in conf["replacements"].items():
            new_text = new_text.replace(old_word, new_link)
        
        try:
            await client.copy_message(
                chat_id=conf["target"],
                from_chat_id=chat_id,
                message_id=message.id,
                caption=new_text
            )
            print(f"✅ Xabar ko'chirildi: {chat_id}")
        except Exception as e:
            print(f"❌ Xatolik ({chat_id}): {e}")

    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except Exception as e:
        print(f"Kritik xatolik: {e}")
