import asyncio
from telebot.async_telebot import AsyncTeleBot
from config import telegram_params
from telebot import TeleBot

temp_folder_path = "temp_files"

# Check token
if not isinstance(telegram_params.bot_token,str):
	raise Exception("Invalid Bot token")
# Init bot
# bot = TeleBot(telegram_params.bot_token)
bot = AsyncTeleBot(telegram_params.bot_token)
# Assign event handlers

@bot.message_handler(commands=['start'])
async def start_message(message):
	print("Hello")
	await bot.send_message(message.chat.id, 'Hello to our voice bot!')

@bot.message_handler()
async def start_message(message):
	print("Hello")
	await bot.send_message(message.chat.id, 'Hello to our voice bot!')

@bot.message_handler(content_types=['voice'])
async def voice_processing(message):
	print("Hello")
	# Processing voice
	file_info = await bot.get_file(message.voice.file_id)
	downloaded_file = await bot.download_file(file_info.file_path)

	# Save voice
	with open(f'{temp_folder_path}/temp_voice.wav', 'wb') as new_file:
		new_file.write(downloaded_file)



print("Run the chatbot")
# Run bot
asyncio.run(bot.polling())
