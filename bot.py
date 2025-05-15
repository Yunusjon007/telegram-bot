import nest_asyncio
nest_asyncio.apply()

import os
from dotenv import load_dotenv
load_dotenv()

import asyncio
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram import Update
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

knowledge_base = """
1. Biz IT xizmatlari ko‘rsatamiz.
2. Ish vaqti: Dushanbadan – Jumagacha, 09:00 – 18:00.
3. Biz bilan bog‘lanish: +998 90 123 45 67
4. Joylashuv: Toshkent shahri, Chilonzor tumani
"""

async def ask_openai(question):
    prompt = f"""
Quyidagi ma’lumotlarga asoslanib foydalanuvchining savoliga javob ber. Agar savol ma’lumotlarga mos kelmasa, "Kechirasiz, bu bo‘yicha ma’lumot yo‘q." deb yoz.

Ma’lumotlar:
{knowledge_base}

Savol:
{question}
"""
    chat_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt]()
