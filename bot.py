import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from groq import Groq

# إعداد السجلات (Logs) لمراقبة عمل البوت
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- الإعدادات (التوكنات جاهزة هسة) ---
TELEGRAM_TOKEN = "8774572251:AAGoWnDhOGkfkKSbVk_N_9XA5-oGW1vcXB4"
GROQ_API_KEY = "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"

# تهيئة عميل Groq
client = Groq(api_key=GROQ_API_KEY)

# دالة الترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا بيك سجاد! أنا بوت الذكاء الاصطناعي الخاص بك، اسألني أي شي.")

# دالة معالجة الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_message}],
            model="llama3-8b-8192",
        )
        response = chat_completion.choices[0].message.content
        await update.message.reply_text(response)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text(f"صار عندي خطأ فني بسيط، جرب مرة ثانية.")

# بناء التطبيق
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# إضافة الأوامر
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

if name == "__main__":
    print("البوت بدأ يشتغل هسة...")
    app.run_polling()
