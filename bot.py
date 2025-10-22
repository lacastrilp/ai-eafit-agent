import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

from agent_core import invoke_agent
from memory_manager import get_chat_history, add_message_to_history

# Cargar variables de entorno
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu agente IA 🤖. Pregúntame algo para empezar.")

# Manejo de mensajes
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_message = update.message.text

    # Guardar mensaje del usuario
    add_message_to_history(user_id, "user", user_message)

    # Recuperar historial
    chat_history = get_chat_history(user_id)

    # Mostrar acción de "escribiendo..."
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    # Invocar al agente (de forma no bloqueante)
    try:
        ai_message = await asyncio.to_thread(invoke_agent, user_message, chat_history)
    except Exception as e:
        print(f"Error invocando al agente: {e}")
        ai_message = "⚠️ Lo siento, hubo un error al procesar tu solicitud."

    # Guardar respuesta del agente
    add_message_to_history(user_id, "ai", ai_message)

    # Enviar respuesta al usuario
    await update.message.reply_text(ai_message)

def main():
    print("🚀 Iniciando el bot...")
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Ejecutar bot
    application.run_polling()

if __name__ == "__main__":
    main()
