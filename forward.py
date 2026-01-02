import os
import asyncio
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# -----------------------------------------------------
# 1. Koyeb-க்கான போலி வெப்சைட் (Dummy Web Server)
# -----------------------------------------------------
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")

def start_web_server():
    # Port 8000-ல் ரன் ஆகும்
    server = HTTPServer(('0.0.0.0', 8000), HealthCheckHandler)
    server.serve_forever()

# வெப்சைட்டை தனி த்ரெட்டில் (Background) ரன் செய்கிறோம்
threading.Thread(target=start_web_server, daemon=True).start()

# -----------------------------------------------------
# 2. Environment Variables & Bot Setup
# -----------------------------------------------------

try:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    SESSION_STRING = os.getenv("SESSION_STRING")

    SOURCE_RAW = os.getenv("SOURCE_CHANNEL")
    if SOURCE_RAW.lstrip('-').isdigit():
        SOURCE_CHANNEL = int(SOURCE_RAW)
    else:
        SOURCE_CHANNEL = SOURCE_RAW

    DEST_GROUP = int(os.getenv("DEST_GROUP"))

except Exception as e:
    print(f"Error reading Environment Variables: {e}")
    exit()

print("Connecting to Telegram...")
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def my_event_handler(event):
    try:
        print(f"New message found in {SOURCE_CHANNEL}...")
        
        # 1. Group-க்கு மெசேஜை அனுப்பு
        sent_msg = await client.send_message(DEST_GROUP, event.message)
        
        # 2. 2 செகண்ட் காத்திரு
        await asyncio.sleep(2) 
        
        # 3. அனுப்பிய மெசேஜுக்கே '/ql2' என்று ரிப்ளை பண்ணு
        await client.send_message(DEST_GROUP, '/ql2', reply_to=sent_msg)
        
        print("✅ Message forwarded and replied /ql2 successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

print("Bot is Active! Waiting for messages...")
client.start()
client.run_until_disconnected()
