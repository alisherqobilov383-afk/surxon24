import sys
import os
import asyncio
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
# Kalitlar faqat username bo'lishi kerak (t.me/ dan keyingi qism)
CONFIG = {
    "tuztuzttt": {  # Misol uchun username
        "target": "surxon_24_live",
        "replacements": {
            "Сурхондарёдаги тезкор янгиликлар каналига обуna бўлинг": "https://t.me/surxon_24_live"
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
        
        if not conf:
            return

        # Matnni o'zgartirish
        text = message.caption or message.text or ""
        new_text = text
        for old_word, new_link in conf["replacements"].items():
            new_text = new_text.replace(old_word, new_link)
        
        try:
            # Xabarni nusxalash
            await client.copy_message(
                chat_id=conf["target"],
                from_chat_id=message.chat.id,
                message_id=message.id,
                caption=new_text[:1024]
            )
            print(f"✅ {chat_username} -> {conf['target']} muvaffaqiyatli!")
        except Exception as e:
            print(f"❌ Xatolik ({chat_username}): {e}")

    await app.start()
    print("🚀 Bot ishga tushdi!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
        pass
