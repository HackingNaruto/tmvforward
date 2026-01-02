import os
import asyncio
from telethon import TelegramClient, events

# -----------------------------------------------------
# Environment Variables-ல் இருந்து தகவல்களை எடுக்கிறோம்
# -----------------------------------------------------

# API ID நம்பர் என்பதால் int() போடுகிறோம்
API_ID = int(os.getenv("API_ID")) 
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING")

# Source Channel ஒருவேளை ID-ஆக இருந்தால் நம்பராக மாற்றும், இல்லையென்றால் பெயராகவே இருக்கும்
SOURCE_CHANNEL_RAW = os.getenv("SOURCE_CHANNEL")
if SOURCE_CHANNEL_RAW.lstrip('-').isdigit():
    SOURCE_CHANNEL = int(SOURCE_CHANNEL_RAW)
else:
    SOURCE_CHANNEL = SOURCE_CHANNEL_RAW

# Destination Group கண்டிப்பா ID தான், அதனால் int() போடுகிறோம்
DEST_GROUP = int(os.getenv("DEST_GROUP"))

# -----------------------------------------------------
# Userbot Setup
# -----------------------------------------------------

if SESSION_STRING:
    from telethon.sessions import StringSession
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
else:
    # லோக்கலில் டெஸ்ட் பண்ணும்போது மட்டும் இது தேவைப்படும்
    client = TelegramClient('myuserbot', API_ID, API_HASH)

print("Userbot Started on Koyeb! 🚀")
print(f"Monitoring: {SOURCE_CHANNEL}")
print(f"Target: {DEST_GROUP}")

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def my_event_handler(event):
    try:
        # 1. Group-க்கு மெசேஜை அனுப்பு
        sent_msg = await client.send_message(DEST_GROUP, event.message)
        
        # 2. 2 செகண்ட் காத்திரு
        await asyncio.sleep(2) 
        
        # 3. /ql2 என்று ரிப்ளை பண்ணு
        await client.send_message(DEST_GROUP, '/ql2', reply_to=sent_msg)
        
        print("File forwarded and replied /ql2 successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

client.start()
client.run_until_disconnected()
