import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from groq import Groq

# إعدادات السجلات (Logs)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# حط التوكنات مالتك هنا (تأكد إنها بين علامات الاقتباس)
TELEGRAM_TOKEN = "أدخل_توكن_بوت_التليجرام_هنا"
GROQ_API_KEY = "أدخل_مفتاح_جروك_هنا"

# تهيئة عميل Groq
client = Groq(api_key=GROQ_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا بيك سجاد! أنا بوت الذكاء الاصطناعي، اسألني أي شي.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    try:
        # إرسال الرسالة إلى Groq
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_message}],
            model="llama3-8b-8192",
        )
        response = chat_completion.choices[0].message.content
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"صار عندي خطأ: {e}")

# البديل للسطر اللي ردته (تشغيل مباشر)
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

print("البوت بدأ يشتغل هسة...")
app.run_polling()
