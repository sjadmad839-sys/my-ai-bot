import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# حط توكن البوت وتوكن Groq هنا
TOKEN = "توكن_بوتك_هنا"
GROQ_API_KEY = "مفتاح_جروق_هنا"

client = Groq(api_key=GROQ_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً سجاد! أنا بوتك المطور. دزلي أي شي (نص أو صورة قريباً) وأنا أجيبك.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": user_text}],
        model="llama3-8b-8192",
    )
    reply = chat_completion.choices[0].message.content
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if name == '__main__':
    main()