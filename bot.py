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

# --- الإعدادات (التوكنات) ---
TELEGRAM_TOKEN = "8774572251:AAGoWnDhOGkfkKSbVk_N_9XA5-oGW1vcXB4"
# حط مفتاح Groq مالتك هنا بين علامات الاقتباس
GROQ_API_KEY = "حط_مفتاح_جروك_هنا" 

# تهيئة عميل Groq
client = Groq(api_key=GROQ_API_KEY)

# دالة الترحيب عند كتابة /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("هلا بيك سجاد! أنا بوت الذكاء الاصطناعي، اسألني أي شي.")

# دالة معالجة الرسائل والرد عليها باستخدام الذكاء الاصطناعي
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    try:
        # إرسال الرسالة إلى نموذج Llama 3 في Groq
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_message}],
            model="llama3-8b-8192",
        )
        response = chat_completion.choices[0].message.content
        await update.message.reply_text(response)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text(f"صار عندي خطأ فني بسيط، جرب مرة ثانية.")

# بناء التطبيق وتشغيله مباشرة
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# إضافة الأوامر والمستمعين
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

if name == "__main__":
    print("البوت بدأ يشتغل هسة...")
    app.run_polling()
