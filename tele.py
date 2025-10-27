# auto_reply.py
import asyncio
from telethon import TelegramClient, events
from datetime import datetime, timedelta

# ==========================
# 🔧 CONFIGURATION
# ==========================
API_ID = 22802017
API_HASH = "47125011540567581b71eaaccd9aedf7"
SESSION_NAME = "berlin_auto_reply"

# Message sent when a user contacts you
WELCOME_MESSAGE = (
    "❤️ 𝙏𝙃𝘼𝙉𝙆𝙎 𝙁𝙊𝙍 𝘾𝙊𝙉𝙏𝘼𝘾𝙏𝙄𝙉𝙂 𝙈𝙀 ❤️\n\n"
    "⚠️❗️𝘾𝙪𝙧𝙧𝙚𝙣𝙩𝙡𝙮 𝙄 𝙖𝙢 𝙤𝙛𝙛𝙡𝙞𝙣𝙚 𝙨𝙤 𝙠𝙞𝙣𝙙𝙡𝙮 𝙬𝙖𝙞𝙩 ✅ "
    "𝙖𝙣𝙙 𝙄 𝙬𝙞𝙡𝙡 𝙨𝙪𝙧𝙚𝙡𝙮 𝙧𝙚𝙥𝙡𝙮 𝙬𝙝𝙚𝙣 𝙄 𝙬𝙞𝙡𝙡 𝙘𝙤𝙢𝙚 𝙤𝙣𝙡𝙞𝙣𝙚 ❗️✅\n\n"
    "🌸 𝙍𝙀𝙂:- @BERLIN_IS_BERLIN"
)

# ==========================
# ⚙️ MAIN LOGIC
# ==========================
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# Store user last message timestamps
user_last_message_time = {}

@client.on(events.NewMessage(incoming=True))
async def handle_private_message(event):
    """Send auto reply only to private users (not bots or groups)."""
    if not event.is_private:
        return  # Ignore groups and channels

    me = await client.get_me()
    if event.sender_id == me.id:
        return  # Ignore your own messages

    user_id = event.sender_id
    current_time = datetime.now()
    last_time = user_last_message_time.get(user_id)

    # Send only once per 24 hours
    if not last_time or (current_time - last_time) >= timedelta(hours=24):
        user_last_message_time[user_id] = current_time
        try:
            await event.respond(WELCOME_MESSAGE)
            print(f"[+] Sent offline message to user {user_id}")
        except Exception as e:
            print(f"[x] Failed to send to {user_id}: {e}")

async def main():
    await client.start()
    print("✅ Auto-reply bot is running... (press Ctrl+C to stop)")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
