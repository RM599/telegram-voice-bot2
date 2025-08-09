import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from gtts import gTTS
from tempfile import NamedTemporaryFile
from deep_translator import GoogleTranslator

# گرفتن توکن از متغیر محیطی
TOKEN = os.getenv("BOT_TOKEN")

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_data[user_id] = {}

    keyboard = [
        [InlineKeyboardButton("🎤 وویس", callback_data='output_voice')],
        [InlineKeyboardButton("✍️ متن", callback_data='output_text')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("می‌خوای خروجی چی باشه؟", reply_markup=reply_markup)

async def output_choice_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    choice = query.data

    if user_id not in user_data:
        user_data[user_id] = {}

    user_data[user_id]['output'] = 'voice' if choice == 'output_voice' else 'text'
    await query.edit_message_text("حالا لطفاً متنت رو بفرست.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in user_data or 'output' not in user_data[user_id]:
        await update.message.reply_text("لطفاً اول با /start شروع کن.")
        return

    user_data[user_id]['text'] = text

    keyboard = [
        [InlineKeyboardButton("🇺🇸 انگلیسی", callback_data='en')],
        [InlineKeyboardButton("🇫🇷 فرانسوی", callback_data='fr')],
        [InlineKeyboardButton("🇩🇪 آلمانی", callback_data='de')],
        [InlineKeyboardButton("🇮🇹 ایتالیایی", callback_data='it')],
        [InlineKeyboardButton("🇪🇸 اسپانیایی", callback_data='es')],
        [InlineKeyboardButton("🇸🇦 عربی", callback_data='ar')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("به چه زبانی ترجمه کنم؟", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    target_lang = query.data
    user_info = user_data.get(user_id, {})
    text = user_info.get('text')
    output_type = user_info.get('output')

    if not text or not output_type:
        await query.message.reply_text("لطفاً با /start شروع کن.")
        return

    translated = GoogleTranslator(source='auto', target=target_lang).translate(text)

    if output_type == 'text':
        await query.message.reply_text(f"ترجمه:\n\n{translated}")
    else:
        tts = gTTS(text=translated, lang=target_lang)
        with NamedTemporaryFile(delete=False, suffix='.mp3') as f:
            tts.save(f.name)
            await query.message.reply_audio(audio=open(f.name, 'rb'), title="Voice Message")
            os.remove(f.name)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(output_choice_callback, pattern="^output_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))

    print("🤖 Bot is running...")
    app.run_polling()
