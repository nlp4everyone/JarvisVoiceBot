from telethon import events
import asyncio
from system_components import Logger

@events.register(events.NewMessage(pattern = "/start"))
async def welcome_handler(event):
    # Important parameter
    chat = await event.get_chat() # Get chat object
    # Define client
    client = event.client
    client_info = await client.get_entity(event.chat_id)

    # Notify
    message = f"User: {event.chat.last_name} (ID: {event.chat_id}) start Welcome event"
    Logger.info(message)

    # Send message back
    images_filename = "images/chatbot_img.png"
    file = await client.upload_file(images_filename)
    welcome_message = """
    Welcome to Jarvis Voice chatbot! \n I can answer your any question with low latency and high precision! 
    """
    await client.send_file(chat, file , caption = welcome_message)