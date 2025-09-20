import os
import logging
import ssl
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from typing import List
from telegram.ext import BaseHandler
from telegram.error import BadRequest

# إعداد التسجيل الأساسي لعمليات البوت
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# استرداد توكن البوت من متغيرات البيئة
BOT_TOKEN = os.getenv("BOT_TOKEN")

# تعريف رابط تطبيق تيليجرام المصغر الخاص بك ورابط القناة الرسمية
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://t.me/Gift_Graphs_bot/Saeed/webapp.com")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/Gift_Graphs/channel.com")

# -----------------
# دوال المساعدة
# -----------------
def create_welcome_keyboard() -> InlineKeyboardMarkup:
    """
    إنشاء لوحة المفاتيح المضمنة مع أزرار WebAppInfo ورابط مباشر
    """
    keyboard = [
        [
            InlineKeyboardButton("Open 🎁", web_app=WebAppInfo(url=MINI_APP_URL)),
            InlineKeyboardButton("Channel 📢", url=CHANNEL_URL)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# -----------------
# معالجات الأوامر والرسائل
# -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    معالج أمر /start
    """
    user_id = update.effective_user.id
    logger.info(f"المستخدم {user_id} بدأ المحادثة أو أرسل أمر /start.")

    # بناء رسالة الترحيب
    message = (
        'Welcome to Gift Graphs! 👋\n\n'
        '📊 The best app for displaying NFT gift prices on Telegram in a simple, modern, and advanced way.\n\n'
        'Official Channel: @Gift_Graphs'
    )

    # بناء لوحة المفاتيح المضمنة
    reply_markup = create_welcome_keyboard()

    try:
        # إرسال الرسالة مع الأزرار بالقوة
        await update.message.reply_text(
            text=message,
            reply_markup=reply_markup,
            parse_mode=None  # تعطيل Markdown لتجنب أي أخطاء
        )
        logger.info(f"تم إرسال رسالة الترحيب مع الأزرار للمستخدم {user_id}.")
        
    except Exception as e:
        logger.error(f"خطأ غير متوقع في إرسال الرسالة: {e}")
        # محاولة إرسال الرسالة بدون أزرار كحل أخير
        try:
            await update.message.reply_text(message)
        except Exception as final_error:
            logger.error(f"فشل إرسال الرسالة تماماً: {final_error}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    معالج أمر /help
    """
    help_message = (
        '**Help Menu**\n'
        '/start - Start a conversation and get the bot info.\n'
        '/help - Show this help menu.\n\n'
        'Mini App Link: https://t.me/Gift_Graphs_bot/Saeed\n'
        'Official Channel: @Gift_Graphs'
    )
    try:
        await update.message.reply_text(help_message, parse_mode='Markdown')
    except BadRequest:
        # إذا فشل Markdown، أرسل بدون تنسيق
        await update.message.reply_text(help_message.replace('**', ''))

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    معالج الرسائل النصية
    """
    await update.message.reply_text("Please use the commands /start or /help.")

def get_bot_handlers() -> List[BaseHandler]:
    """
    ينشئ ويهيئ قائمة بـ handlers الخاصة بالبوت.
    """
    # تهيئة SSL لتجنب المشاكل المحتملة في بعض البيئات
    ssl.OPENSSL_VERSION = ssl.OPENSSL_VERSION.replace("LibreSSL", "OpenSSL")
    
    # إضافة معالجات الأوامر
    return [
        CommandHandler("start", start),
        CommandHandler("help", help_command),
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    ] 
