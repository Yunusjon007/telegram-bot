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
"Kredit Markazi"ning asosiy vazifasi mijozlar uchun istalgan turdagi kreditni 1tagina passport evaziga olib berishdan iborat.
Kredit turlari:
1. Uy uchun ipoteka krediti (1 mlrd so'mgacha bo'lgan uylar uchun bank orqali kredit rasmiylashtiriladi)
2. Avtomobil uchun kredit
3. Kichik summadagi kredit — 5 mln dan boshlab 50 mln gacha
4. Kredit tarixi yomon bo'lganlar uchun ham olib bera olamiz

Kredit foiz stavkasi haqida xodimlar to‘liq ma’lumot beradi.
Agar mijozlarning kredit tarixi yomon bo‘lsa, kafil yoki garov evaziga 3 mlrd so‘mgacha kredit olib berish mumkin.

Mashina garovi evaziga kredit olish uchun mashina 2016-yildan keyingi bo‘lishi kerak.

Telefon raqam: +99878 555–22–55
Telegram admin: https://t.me/kreditmarkazi_admin
Manzil: Toshkent shahri, Glinka ko‘chasi 33-uy
Lokatsiya: https://yandex.uz/maps/10335/tashkent/?ll=69.262391%2C41.286199&mode=whatshere&whatshere%5Bpoint%5D=69.262208%2C41.286231&whatshere%5Bzoom%5D=16&z=19
"""

async def ask_openai(question):
    prompt = f"""
Faqat quyidagi ma’lumotlarga asoslanib javob ber. Javob faqat o‘zbek lotin tilida bo‘lsin. Agar savol ma’lumotlarga to‘g‘ri kelmasa, "Kechirasiz, siz so‘ragan savolga to‘g‘ridan-to‘g‘ri javob topilmadi, ammo biz istalgan turdagi kreditni pasport asosida olib bera olamiz. Uy ipotekasi, avtomobil krediti, kichik miqdordagi kreditlar va hatto yomon kredit tarixiga ega mijozlar uchun ham yechimlarimiz bor. Qo‘shimcha ma’lumot uchun +99878 555–22–55 raqamiga murojaat qiling yoki @kreditmarkazi_admin bilan bog‘laning." deb yoz.

Ma’lumotlar:
{knowledge_base}

Savol:
{question}
"""
    chat_response = client.chat.completions.create(
        model="gpt-4o",
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
