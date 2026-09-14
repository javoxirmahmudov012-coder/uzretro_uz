from extensions import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Mijoz ma'lumotlari
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_telegram = db.Column(db.String(100), nullable=True)
    customer_email = db.Column(db.String(120), nullable=True)
    customer_address = db.Column(db.String(255), nullable=True)
    
    # Xizmat ma'lumotlari
    service_type = db.Column(db.String(50), nullable=False)  
    # vhs_to_flash, vhs_to_cloud, vhs_to_harddisk, harddisk_backup
    
    quantity = db.Column(db.Integer, default=1)
    description = db.Column(db.Text, nullable=True)
    
    # Holat
    status = db.Column(db.String(30), default='new')
    # new, accepted, processing, ready, delivered, cancelled
    
    # Narx va to'lov
    price = db.Column(db.Float, nullable=True)
    is_paid = db.Column(db.Boolean, default=False)
    payment_method = db.Column(db.String(50), default='card')  # card, cash, bank
    
    # Vaqt
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Telegram xabar yuborildi?
    telegram_notified = db.Column(db.Boolean, default=False)
    
    def status_badge(self):
        badges = {
            'new': ('🆕 Yangi', 'primary'),
            'accepted': ('✅ Qabul qilindi', 'info'),
            'processing': ('⚙️ Jarayonda', 'warning'),
            'ready': ('🎉 Tayyor', 'success'),
            'delivered': ('📦 Topshirildi', 'secondary'),
            'cancelled': ('❌ Bekor', 'danger'),
        }
        return badges.get(self.status, ('❓ Noma\'lum', 'secondary'))
    
    def service_name(self):
        names = {
            'vhs_to_flash': '📼 VHS → Fleshka',
            'minidv_video8': '📹 MiniDV & Video8',
            'vhs_to_harddisk': '💾 VHS → Hard disk (mijozdan)',
            'dvd_disk': '💿 DVD / CD Disklar ($30+)',
            'harddisk_backup': '🗄️ Hard disk nusxa',
        }
        return names.get(self.service_type, self.service_type)
    
    def payment_method_name(self):
        methods = {
            'card': '💳 Karta orqali (Click / Payme / Uzum)',
            'cash': '💵 Naqd pul (Topshirilganda)',
            'bank': '🏦 Bank o\'tkazmasi (Hisob raqam)',
        }
        return methods.get(self.payment_method, self.payment_method or 'Ko\'rsatilmagan')
    
    def __repr__(self):
        return f'<Order #{self.id} - {self.customer_name}>'
