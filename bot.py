import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Import our logic
from agent_core import invoke_agent
from memory_manager import get_chat_history, add_message_to_history

# Load environment variables
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Function for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu agente IA. Pregúntame algo.")

# Main function to handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_message = update.message.text

    # 1. Save the user's message in memory
    add_message_to_history(user_id, "user", user_message)

    # 2. Retrieve chat history (including the new message)
    chat_history = get_chat_history(user_id)

    # 3. Invoke the agent (the brain)
    try:
        # This may take a few seconds; Telegram might show "typing..."
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action="typing"
        )

        response = invoke_agent(user_message, chat_history)
        ai_message = response["output"]

    except Exception as e:
        print(f"Error invoking the agent: {e}")
        ai_message = "Lo siento, tuve un error al procesar tu solicitud."

    # 4. Save the AI's response in memory
    add_message_to_history(user_id, "ai", ai_message)

    # 5. Send the response to the user
    await update.message.reply_text(ai_message)

def main():
    print("Iniciando el bot...")
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
