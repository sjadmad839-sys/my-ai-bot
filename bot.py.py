import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq
import os

# 1. المعلومات الأساسية
TELEGRAM_TOKEN = "8774572251:AAGoWnDhOGkfkKSbVk_N_9XA5-oGW1vcXB4"
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً سجاد! أنا بوتك المطوّر. دزلي رسالة أو ملف (PDF/Text) وحتدلل.")

async def handle_docs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_path = f"downloads/{update.message.document.file_name}"
    os.makedirs("downloads", exist_ok=True)
    await file.download_to_drive(file_path)
    
    await update.message.reply_text("جاري قراءة الملف وتلخيصه، انتظرني ثواني...")
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()[:4000] # نأخذ أول 4000 حرف للتلخيص

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": f"لخص لي هذا النص بالعربي: {content}"}]
    )
    await update.message.reply_text(completion.choices[0].message.content)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": update.message.text}]
        )
        await update.message.reply_text(completion.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

# التشغيل
app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.add_handler(MessageHandler(filters.Document.ALL, handle_docs))

print("البوت المطوّر شغال هسة...")
app.run_polling()

