import sys
import os
import asyncio
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
# Har bir manba kanalini shu yerga qo'shing
CONFIG = {
    "@SurxondaryoRasmiy": {
        "target": "@surxon_24_live",
        "replacements": {
            "Сурхондарёдаги тезкор янгиликлар каналига обуна бўлинг": "https://t.me/surxon_24_live",
            "MEqqwqwqwDIA": "https://t.me/eltua",
            "qwqwqwqw": "https://x.com/eltz"
        }
    },
    "@Termiz_yangiliklari": {
        "target": "@surxon_24_live",
        "replacements": {
            "Surxondaryoning eng aktiv kanali👇": "https://t.me/surxon_24_live",
            "Facebook": "https://www.facebook.com/profile.php?id=61585wqqwd818251235"
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
        chat_username = f"@{message.chat.username}"
        conf = CONFIG.get(chat_username)
        
        # Matnni yoki captionni olish
        text = message.caption or message.text or ""
        
        # Replacements (Almashtirish) jarayoni
        new_text = text
        for old_word, new_link in conf["replacements"].items():
            new_text = new_text.replace(old_word, new_link)
        
        try:
            # Media yoki matnli xabarni ko'chirish
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
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot())