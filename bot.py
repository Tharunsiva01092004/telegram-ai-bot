import openai
import logging
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters
)

# 🔑 Replace with your API keys
OPENAI_API_KEY = "gp-3.5-turbo"
TELEGRAM_BOT_TOKEN = "7897959677:AAHCcp-2sEAscrsJ-ggoU0IMX7NluAyBiOI"

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Set up logging (for debugging)
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Function to get AI response from OpenAI's GPT
async def get_gpt_response(user_message):
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",  # Corrected model name
            messages=[{"role": "user", "content": user_message}],
            max_tokens=200,
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error(f"Error in OpenAI API call: {e}")
        return "Sorry, I am having trouble responding right now."

# Function to handle incoming messages
async def handle_message(update: Update, context) -> None:
    user_text = update.message.text
    logging.info(f"User said: {user_text}")

    # Get AI response
    ai_response = await get_gpt_response(user_text)

    # Send reply back to user
    await update.message.reply_text(ai_response)

# Function to handle "/start" command
async def start(update: Update, context) -> None:
    await update.message.reply_text("Hello! I'm your AI chatbot 🤖. How can I assist you today?")

# Main function to set up the bot
async def main():
    # Set up the Telegram bot using ApplicationBuilder (new syntax)
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot (special handling for Colab)
    logging.info("🤖 Bot is running...")
    await app.initialize()
    await app.start()
    await app.run_polling()  # Replaced deprecated updater usage

# 🚀 Run the bot (works in Colab)
if __name__ == "__main__":
    try:
        asyncio.run(main())  # ✅ Safe for scripts
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.create_task(main())  # ✅ Safe for Colab & Jupyter
