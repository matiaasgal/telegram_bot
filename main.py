import os
import asyncio
from telegram import Bot
from icalevents.icalevents import events

from datetime import datetime, date, timedelta
import pytz


TOKEN_BOT = os.getenv("TOKEN_BOT")
CHAT_ID = os.getenv("CHAT_ID")
ICAL = os.getenv("ICAL")

print("TOKEN:", bool(TOKEN_BOT))
print("CHAT_ID:", bool(CHAT_ID))
print("ICAL:", bool(ICAL))

if not TOKEN_BOT or not CHAT_ID or not ICAL:
    print("Error: Falta configurar alguna variable de entorno")
    exit(1)

async def verificar_eventos():
    tz = pytz.timezone('America/Santiago')
    utc = pytz.utc

    manana = datetime.now(tz) + timedelta(days=1)
    inicio = manana.replace(hour=00, minute=00, second=00)
    fin = manana.replace(hour=23, minute=59, second=59)

    inicio_utc = inicio.astimezone(utc)
    fin_utc = fin.astimezone(utc)

    try:
        lista_eventos = events(ICAL, start=inicio_utc, end=fin_utc)
  
        if not lista_eventos:
            print("No hay eventos para mañana")
            return

        mensaje = "Mañana tienes el siguiente evento: "
        for evento in lista_eventos:
            hora = evento.start.strftime("%H:%M")
            mensaje += f"• {evento.summary} a las {hora} hrs\n"

        bot = Bot(token=TOKEN_BOT)
        await bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode="Markdown")
        print('Recordatorio enviado')

    except Exception as e:
        print(f"Error al leer el calendario: {e}")


if __name__ == "__main__":
    asyncio.run(verificar_eventos())
