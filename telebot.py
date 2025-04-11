import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Get API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Check if Telegram bot token is set
if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set. Check your .env file.")

# Model name
MODEL_NAME = "gpt-3.5-turbo"

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

class Reference:
    """A class to store previously generated responses from ChatGPT API."""
    def __init__(self):
        self.response = ""

reference = Reference()

def clear_past():
    """Clears the previous conversation and context."""
    reference.response = ""

# Register message handlers
@dp.message(Command("start"))
async def welcome(message: Message):
    """Handles the /start command."""
    await message.answer("Hi\n I am Tele Bot! Created by Me. How can I assist you?")

@dp.message(Command("clear"))
async def clear(message: Message):
    """Handles the /clear command to reset chat history."""
    clear_past()
    await message.answer("I've cleared the past conversation and context.")

@dp.message(Command("help"))
async def helper(message: Message):
    """Handles the /help command to display help menu."""
    help_text = (
        "Hi There, I'm a ChatGPT Telegram bot created by ME!\n\n"
        "Please use the following commands:\n"
        "/start - Start the conversation\n"
        "/clear - Clear the past conversation and context\n"
        "/help - Show this help menu\n\n"
        "I hope this helps! 😊"
    )
    await message.answer(help_text)

@dp.message()
async def chatgpt(message: Message):
    """Handles user messages and queries ChatGPT API."""
    print(f">>> USER: \n\t{message.text}")

    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=[
            {"role": "assistant", "content": reference.response},  # Previous response
            {"role": "user", "content": message.text},  # User query
        ],
    )

    # Store response
    reference.response = response["choices"][0]["message"]["content"]
    
    print(f">>> chatGPT: \n\t{reference.response}")
    await message.answer(reference.response)

# Start bot
async def main():
    """Main function to start the bot."""
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
