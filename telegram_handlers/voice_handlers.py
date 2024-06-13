import os.path
from telethon import events
import time,json
from system_components import Logger
from chat_modules.llamaindex.intergrations import IntergrationsChatModule,ChatModelProvider
from speech2text_modules.intergrations import DeepGramS2TModule
from config import telegram_params

# Get approved users
with open("./approved_users.json",'r') as f:
    data = json.load(f)
approved_users = list(dict(data).values())

# Define module
chat_module = IntergrationsChatModule(service_name = ChatModelProvider.GROQ, model_name = "llama3-8b-8192")
s2t_module = DeepGramS2TModule()

async def response_answer(question: str, client, event):
    # Important parameter
    chat = await event.get_chat()  # Get chat object

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
    # Log state
    Logger.info(f"User {event.chat.last_name} (ID: {event.chat_id}) Question: {question}")

    # Response
    await response_answer(question = question, event = event, client = client)

@events.register(events.NewMessage(func = lambda e: e.message.voice))
async def voice_response(event):
    # Define user id
    user_id = event.message.chat_id
    # Define client
    client = event.client
    chat = await event.get_chat()

    # Get date
    event_date = event.message.date
    # Convert to format
    voice_date = event_date.strftime("%H:%M_%Y-%m-%d")

    audio_name = f"audio_{user_id}_{voice_date}.wav"
    audio_path = os.path.join(telegram_params.audio_dir,audio_name)

    # Download voice
    await event.message.download_media(file = audio_path)


    try:
        # Get transcription
        transcription = s2t_module.transcribe(audio_path)

        # Send response
        async with client.action(chat, 'typing') as action:
            await client.send_message(chat, f"Your COMMAND: {transcription}")

        # Log state
        Logger.info(f"User {event.chat.last_name} (ID: {event.chat_id}) Question: {transcription}")

        # Response
        await response_answer(question=transcription, event=event, client=client)

    except:
    # Send message
        async with client.action(chat, 'typing') as action:
            await client.send_message(chat, f"Wrong with response from speech to text module")





