import asyncio
from telegram import Bot
import os
from icalevents.icalevents import events
from datetime import datetime, timedelta

TOKEN = os.getenv("TOKEN_BOT")
CHAT_ID = os.getenv("CHAT_ID")
ICAL_URL = os.getenv("ICAL")

async def verificar_eventos():
    hoy = datetime.now()
    manana = hoy + timedelta(days=1)

    try:
        lista_eventos = events(ICAL_URL, start=manana, end=manana)
        
        if not lista_eventos:
            print("No hay eventos para mañana")
            return

        mensaje = "Mañana tienes el siguiente evento: "
        for evento in lista_eventos:
            hora = evento.start.strftime("%H:%M")
            mensaje += f"* {evento.summary} a las {hora} \n"

        bot = Bot(token=TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode="Markdown")
        print('Recordatorio enviado')

    except Exception as e:
        print(f"Error al leer el calendario: {e}")


if __name__ == "__main__":
    asyncio.run(verificar_eventos())
