import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters

# --- 1. SERVIDOR WEB PARA RENDER ---
# Esto evita que Render apague el bot por inactividad.
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot vivo y coleando"

def run_web():
    # Render asigna un puerto automáticamente en la variable de entorno PORT
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

# --- 2. LÓGICA DE TRANSFORMACIÓN ---
# Eliminada la 'ñ' y sincronizadas las longitudes (62 caracteres cada una)
letras_normales = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
letras_font     = "ɑbcdefghijklmnopqrstuvwxtzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def transformar_texto(texto):
    resultado = ""
    # Iteramos directamente sobre el texto recibido
    for caracter in texto:
        if caracter in letras_normales:
            posicion = letras_normales.index(caracter)
            resultado += letras_font[posicion]
        else:
            # Si es espacio, símbolo o la 'ñ', se mantiene original
            resultado += caracter
    return resultado

async def procesar_mensaje(update: Update, context):
    # Verificamos que el mensaje contenga texto
    if update.message and update.message.text:
        texto_convertido = transformar_texto(update.message.text)
        await update.message.reply_text(texto_convertido)

# --- 3. ARRANQUE DEL BOT ---
if __name__ == '__main__':
    # Iniciamos el servidor Flask en un hilo secundario (daemon)
    threading.Thread(target=run_web, daemon=True).start()

    # Obtenemos el Token desde las variables de entorno
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    if not TOKEN:
        print("ERROR: No se encontró la variable TELEGRAM_TOKEN en el entorno.")
    else:
        # Configuramos el ApplicationBuilder
        app_bot = ApplicationBuilder().token(TOKEN).build()
        
        # Filtro: Solo mensajes de texto que no sean comandos
        app_bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), procesar_mensaje))
        
        print("Bot encendido... Escuchando mensajes.")
        app_bot.run_polling()
