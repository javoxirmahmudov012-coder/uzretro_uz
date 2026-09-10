import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uzretro-secret-key-2024'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///uzretro.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN') or ''
    TELEGRAM_ADMIN_CHAT_ID = os.environ.get('TELEGRAM_ADMIN_CHAT_ID') or ''
    
    # Biznes ma'lumotlari
    BUSINESS_NAME = "UzRetro.uz"
    BUSINESS_PHONE = "+998 87 770 02 33"
    BUSINESS_ADDRESS = "Toshkent shahri, Chilonzor tumani, Qatortol ko'chasi 60B, Biznes Markaz"
    BUSINESS_LANDMARK = "Parus binosi (savdo markazi)"
    BUSINESS_TELEGRAM = "https://t.me/uzretrouz"
    BUSINESS_INSTAGRAM = "https://instagram.com/uzretro.uz"
    BUSINESS_TELEGRAM_USERNAME = "@uzretrouz"
