import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# --- 1. EL TRUCO PARA RENDER ---
# Creamos una web falsa para que Render no nos apague
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot vivo y coleando"

def run_web():
    # Render usa el puerto 10000 por defecto o el que te asigne
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

# --- 2. TU LÓGICA DE FUENTES (La que te gustó) ---
letras_normales = "abcdefghijklmnñopqrstuvwxtzABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789"
letras_font =     ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h','i', 'j','k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 't', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'Ñ', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def transformar_texto(texto):
    resultado = ""
    for caracter in texto():
        if caracter in letras_normales:
            posicion = letras_normales.index(caracter)
            resultado += letras_font[posicion]
        else:
            resultado += caracter
    return resultado

async def procesar_mensaje(update, context):
    texto_final = transformar_texto(update.message.text)
    await update.message.reply_text(texto_final)

# --- 3. ARRANQUE ---
if __name__ == '__main__':
    # Lanzamos la web falsa en un "hilo" aparte para que no moleste al bot
    threading.Thread(target=run_web).start()

    # Arrancamos el bot de Telegram
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    app_bot = ApplicationBuilder().token(TOKEN).build()
    
    app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), procesar_mensaje))
    
    print("Bot encendido en modo ahorro...")
    app_bot.run_polling()
