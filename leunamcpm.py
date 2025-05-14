python
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Configuración del logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Aquí debes reemplazar 'TU_TOKEN_DE_TELEGRAM' con tu token real
TOKEN = "7912969152:AAFaIvqm39uPL2C7PXS2xInVITo-TwZ_F-8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando para iniciar el bot."""
    await update.message.reply_text(f'Hola {update.effective_user.first_name}! Soy tu bot de Telegram.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando para mostrar ayuda."""
    await update.message.reply_text('Este es un bot de prueba para verificar tu token de Telegram.')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Repite el mensaje del usuario."""
    await update.message.reply_text(update.message.text)

def main() -> None:
    """Función principal para iniciar el bot."""
    # Crea la aplicación y pasa el token
    application = ApplicationBuilder().token(TOKEN).build()

    # Registra los handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # En cualquier otro mensaje, responde con eco
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Inicia el bot
    print("Bot iniciado. Presiona Ctrl+C para detener.")
    application.run_polling()

if __name__ == '__main__':
    main()