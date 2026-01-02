import os
import asyncio
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# Logging வசதி (ஏதாவது பிழை வந்தால் பார்க்க உதவும்)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# -----------------------------------------------------
# Environment Variables-ல் இருந்து தகவல்களை எடுக்கிறோம்
# -----------------------------------------------------

try:
    # API ID மற்றும் Hash (கட்டாயம் தேவை)
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    SESSION_STRING = os.getenv("SESSION_STRING")

    # Source Channel (Username ஆக இருந்தால் String, ID ஆக இருந்தால் Int ஆக மாற்றும்)
    SOURCE_RAW = os.getenv("SOURCE_CHANNEL")
    if SOURCE_RAW.lstrip('-').isdigit():
        SOURCE_CHANNEL = int(SOURCE_RAW)
    else:
        SOURCE_CHANNEL = SOURCE_RAW

    # Destination Group (கண்டிப்பா ID தான், அதனால் int() போடுகிறோம்)
    DEST_GROUP = int(os.getenv("DEST_GROUP"))

except Exception as e:
    print(f"Error reading Environment Variables: {e}")
    print("Please check your Koyeb Settings!")
    exit()

# -----------------------------------------------------
# Userbot Setup
# -----------------------------------------------------

print("Connecting to Telegram...")

# Session String வைத்து Connect செய்தல்
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def my_event_handler(event):
    try:
        # மெசேஜ் வந்தால் பிரிண்ட் பண்ணும்
        print(f"New message found in {SOURCE_CHANNEL}...")

        # 1. Group-க்கு மெசேஜை அனுப்பு (Forward with copy to avoid forwarded tag if needed, or simple send)
        # இங்கே send_message பயன்படுத்துகிறோம், இது file-ஐ அப்படியே அனுப்பும்
        sent_msg = await client.send_message(DEST_GROUP, event.message)
        
        # 2. 2 செகண்ட் காத்திரு (File upload ஆக டைம் குடுக்குறோம்)
        await asyncio.sleep(2) 
        
        # 3. அனுப்பிய மெசேஜுக்கே '/ql2' என்று ரிப்ளை பண்ணு
        await client.send_message(DEST_GROUP, '/ql2', reply_to=sent_msg)
        
        print("✅ Message forwarded and replied /ql2 successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

print("Bot is Active! Waiting for messages...")
client.start()
client.run_until_disconnected()
