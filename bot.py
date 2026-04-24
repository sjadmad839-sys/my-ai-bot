import logging
import base64
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from groq import Groq

# 1. التوكنات
TELEGRAM_TOKEN = "8774572251:AAHxLjXmTzZFZExwDj5rRj9HWgppK8uVLQM"
GROQ_API_KEY = "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"

logging.basicConfig(level=logging.INFO)
client = Groq(api_key=GROQ_API_KEY)

# وظيفة الصور مع محاولة ذكية لعدة موديلات
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("دا أحاول أشوف الصورة بكل الطرق المتاحة...")
    try:
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        base64_image = base64.b64encode(photo_bytes).decode('utf-8')

        # قائمة الموديلات الممكنة للرؤية
        vision_models = ["llama-3.2-11b-vision-preview", "llama-3.2-90b-vision-preview"]
        
        response = None
        for model_name in vision_models:
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": [{"type": "text", "text": "اشرح الصورة بالعربي"}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}]}],
                )
                if response: break 
            except:
                continue

        if response:
            await update.message.reply_text(response.choices[0].message.content)
        else:
            await update.message.reply_text("عذراً، ميزة الصور متوقفة حالياً من سيرفر Groq لحسابك. جرب ترسل نص.")
            
    except Exception as e:
        await update.message.reply_text(f"خطأ تقني: {e}")

# وظيفة النصوص (المضمونة)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": update.message.text}],
            model="llama-3.3-70b-versatile",
        )
        await update.message.reply_text(chat_completion.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ في الرد النصي: {e}")

# التشغيل
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler('start', lambda u, c: u.message.reply_text("البوت شغال! أرسل نصاً أو صورة.")))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

print("البوت شغال الآن.. جرب النص أولاً.")
app.run_polling()
