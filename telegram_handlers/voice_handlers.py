from telethon import events
import time,json
from system_components import Logger
from chat_modules.llamaindex.intergrations import IntergrationsChatModule,ChatModelProvider

# Get approved users
with open("./approved_users.json",'r') as f:
    data = json.load(f)
approved_users = list(dict(data).values())

# Define params
chat_module = IntergrationsChatModule(service_name = ChatModelProvider.GROQ, model_name = "llama3-8b-8192")
system_prompt = """
You're are helpful assistant, be kind, non biased and toxic.
"""

async def response_answer(question: str, client, event):
    # Important parameter
    chat = await event.get_chat()  # Get chat object

    Logger.info(f"User {event.chat.last_name} (ID: {event.chat_id}) Question: {question}")
    # Begin Time
    beginTime = time.time()
    # Get response
    response = await chat_module.achat(user_prompt = question)
    endTime = time.time() - beginTime
    endTime = round(endTime, 2)

    # Convert to str
    response = response.message.content
    # Log answer
    Logger.info(f"User {event.chat.last_name} (ID: {event.chat_id}) Answer: {response} \n( Response in {endTime}s)")

    # Send message
    async with client.action(chat, 'typing') as action:
        await client.send_message(chat, response)

@events.register(events.NewMessage(pattern = r"^/start", from_users = approved_users))
async def welcome_response(event):

    # With no match
    if event.pattern_match != None:
        # Important parameter
        chat = await event.get_chat() # Get chat object
        # Define client
        client = event.client
        # Notify
        message = f"User: {event.chat.last_name} (ID: {event.chat_id}) join the chat!"
        Logger.info(message)

        # Send message back
        images_filename = "images/chatbot_img.png"
        file = await client.upload_file(images_filename)
        welcome_message = """
        Welcome to Jarvis Voice chatbot! \n I can answer your any question with low latency and high precision! 
        """
        await client.send_file(chat, file , caption = welcome_message)

@events.register(events.NewMessage(pattern = r"[^/]"))
async def question_response(event):
    # Response text question event

    # Define client
    client = event.client
    # Get question
    question = event.message.message

    # Response
    await response_answer(question = question,event = event,client = client)

@events.register(events.NewMessage(func = lambda e: e.message.voice))
async def voice_response(event):
    # Define user id
    user_id = event.message.chat_id

    # Get date
    event_date = event.message.date
    # Convert to format
    voice_date = event_date.strftime("%H:%M_%Y-%m-%d")

    audio_name = f"audio_{user_id}_{voice_date}.wav"
    # Download voice
    await event.message.download_media(file=audio_name)