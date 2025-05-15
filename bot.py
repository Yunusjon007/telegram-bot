import nest_asyncio
nest_asyncio.apply()

import os
from dotenv import load_dotenv
load_dotenv()

import asyncio
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
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
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    return chat_response.choices[0].message.content.strip()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    print(f"Foydalanuvchidan kelgan: {user_msg}")
    reply = await ask_openai(user_msg)
    print(f"Yuboriladigan javob: {reply}")
    await update.message.reply_text(reply)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot ishga tushdi ✅")

async def main():
    app = Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
