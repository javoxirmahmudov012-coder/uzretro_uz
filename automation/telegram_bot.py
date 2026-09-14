"""
UzRetro.uz Telegram Bot
Yangi buyurtmalar haqida xabar beradi va mijozlar bilan muloqot qiladi
"""
import os, sys, requests as req_lib
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
ADMIN_CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID', '')


# ======= SINXRON XABAR YUBORISH =======

def send_telegram_message(text, chat_id=None, parse_mode='HTML'):
    """Telegramga xabar yuborish"""
    if not TOKEN:
        print("TELEGRAM_BOT_TOKEN sozlanmagan!")
        return False
    target = chat_id or ADMIN_CHAT_ID
    if not target:
        print("TELEGRAM_ADMIN_CHAT_ID sozlanmagan!")
        return False
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {'chat_id': target, 'text': text, 'parse_mode': parse_mode, 'disable_web_page_preview': True}
    try:
        r = req_lib.post(url, json=data, timeout=10)
        result = r.json()
        if result.get('ok'):
            return True
        print(f"Telegram xato: {result.get('description')}")
        return False
    except Exception as e:
        print(f"Telegram ulanish xatosi: {e}")
        return False


def send_new_order_notification(order):
    """Yangi buyurtma kelganda admin'ga xabar"""
    msg = (
        f"YANGI BUYURTMA #{order.id}\n"
        f"Ism: {order.customer_name}\n"
        f"Tel: {order.customer_phone}\n"
        f"Email: {order.customer_email or 'Yoq'}\n"
        f"Xizmat: {order.service_name()}\n"
        f"Miqdor: {order.quantity} ta\n"
        f"Izoh: {order.description or 'Yoq'}\n"
        f"Vaqt: {order.created_at.strftime('%d.%m.%Y %H:%M')}"
    )
    return send_telegram_message(msg)


def send_order_ready_notification(order):
    """Buyurtma tayyor bo'lganda xabar"""
    msg = (
        f"BUYURTMA TAYYOR! #{order.id}\n"
        f"Mijoz: {order.customer_name}\n"
        f"Tel: {order.customer_phone}\n"
        f"Xizmat: {order.service_name()}"
    )
    return send_telegram_message(msg)


# ======= BOT POLLING =======

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {'timeout': 30}
    if offset:
        params['offset'] = offset
    try:
        r = req_lib.get(url, params=params, timeout=35)
        return r.json().get('result', [])
    except:
        return []


def handle_message(message):
    chat_id = str(message['chat']['id'])
    text = message.get('text', '')
    first_name = message['chat'].get('first_name', 'Foydalanuvchi')
    print(f"[{chat_id}] {first_name}: {text}")

    if text == '/start':
        reply = (
            f"Assalomu alaykum, {first_name}!\n\n"
            f"UzRetro.uz botiga xush kelibsiz!\n\n"
            f"VHS kasseta, betamax va boshqa eski videolaringizni\n"
            f"fleshka yoki hard diskka 100% maxfiy o'tkazamiz.\n\n"
            f"Buyurtma: uzretro.uz\n"
            f"Yordam: /help"
        )
        send_telegram_message(reply, chat_id=chat_id)
        if chat_id != ADMIN_CHAT_ID:
            send_telegram_message(f"Yangi foydalanuvchi: {first_name} (ID: {chat_id})")

    elif text == '/help':
        reply = (
            "Xizmatlarimiz:\n"
            "- VHS > Fleshka\n"
            "- MiniDV & Video8\n"
            "- VHS > Hard disk\n\n"
            "Buyurtma: uzretro.uz"
        )
        send_telegram_message(reply, chat_id=chat_id)

    elif text == '/myid':
        send_telegram_message(f"Sizning ID: {chat_id}", chat_id=chat_id)

    else:
        send_telegram_message(
            f"Xabar: {first_name} ({chat_id}): {text}"
        )
        send_telegram_message(
            "Xabaringiz qabul qilindi! Tez orada javob beramiz.",
            chat_id=chat_id
        )


def run_bot():
    """Botni polling rejimida ishga tushirish"""
    print(f"UzRetro.uz Bot ishga tushdi!")
    print(f"Token: {TOKEN[:20]}...")
    print("Ctrl+C bilan tuxtatish\n")
    offset = None
    while True:
        try:
            updates = get_updates(offset)
            for update in updates:
                offset = update['update_id'] + 1
                if 'message' in update:
                    handle_message(update['message'])
        except KeyboardInterrupt:
            print("Bot tuxtatildi.")
            break
        except Exception as e:
            print(f"Xato: {e}")
            import time; time.sleep(5)


if __name__ == '__main__':
    if not TOKEN:
        print("TELEGRAM_BOT_TOKEN topilmadi!")
        sys.exit(1)
    run_bot()
