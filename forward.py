import os
import asyncio
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from aiohttp import web

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# -----------------------------------------------------
# 1. Environment Variables Setup
# -----------------------------------------------------
try:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    SESSION_STRING = os.getenv("SESSION_STRING")

    SOURCE_RAW = os.getenv("SOURCE_CHANNEL")
    # சேனல் ID ஆக இருந்தால் int ஆக மாற்றும்
    if SOURCE_RAW.lstrip('-').isdigit():
        SOURCE_CHANNEL = int(SOURCE_RAW)
    else:
        SOURCE_CHANNEL = SOURCE_RAW

    DEST_GROUP = int(os.getenv("DEST_GROUP"))

except Exception as e:
    print(f"Error reading Environment Variables: {e}")
    exit()

# -----------------------------------------------------
# 2. Web Server Setup (aiohttp) - இதுதான் முக்கியம்!
# -----------------------------------------------------
async def web_handler(request):
    return web.Response(text="Bot is Running Successfully!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', web_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    # Port 8000-ல் சர்வரை ஸ்டார்ட் செய்கிறோம்
    site = web.TCPSite(runner, '0.0.0.0', 8000)
    await site.start()
    print("✅ Web Server started on Port 8000")

# -----------------------------------------------------
# 3. Telegram Bot Setup
# -----------------------------------------------------
print("Connecting to Telegram...")
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def my_event_handler(event):
    try:
        print(f"New message found in {SOURCE_CHANNEL}...")
        
        # 1. மெசேஜை அனுப்பு
        sent_msg = await client.send_message(DEST_GROUP, event.message)
        
        # 2. சிறிது நேரம் காத்திரு
        await asyncio.sleep(2) 
        
        # 3. ரிப்ளை அனுப்பு
        await client.send_message(DEST_GROUP, '/ql1', reply_to=sent_msg)
        
        print("✅ Message forwarded and replied /ql2 successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

# -----------------------------------------------------
# 4. Main Runner
# -----------------------------------------------------
async def main():
    # வெப் சர்வரை ஸ்டார்ட் செய்
    await start_web_server()
    
    # பாட்டை ஸ்டார்ட் செய்
    await client.start()
    print("🚀 Bot is Active and Web Server is Listening!")
    
    # பாட் நிற்கும் வரை ஓட விடு
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
