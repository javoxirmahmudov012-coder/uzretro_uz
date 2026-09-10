import os
from flask import Flask
from config import Config
from extensions import db, login_manager

def _create_default_admin(app):
    """Standart admin yaratish (birinchi ishga tushirishda)"""
    from models.user import AdminUser
    
    if not AdminUser.query.filter_by(username='admin').first():
        admin_user = AdminUser(username='admin')
        admin_user.set_password('uzretro2024')
        db.session.add(admin_user)
        db.session.commit()
        print("[OK] Admin yaratildi: login=admin, parol=uzretro2024")
        print("[!]  Birinchi kirishdan song parolni ozgartiring!")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Extension'larni ulash
    db.init_app(app)
    login_manager.init_app(app)
    
    # Blueprint'larni ro'yxatdan o'tkazish
    from routes.main import main
    from routes.admin import admin
    app.register_blueprint(main)
    app.register_blueprint(admin)
    
    # Ma'lumotlar bazasini yaratish
    with app.app_context():
        db.create_all()
        _create_default_admin(app)
    
    return app

# Vercel serverless uchun global app obyekti
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    print("\n" + "="*50)
    print("UzRetro.uz sayt ishga tushdi!")
    print(f"Sayt: http://localhost:{port}")
    print(f"Admin: http://localhost:{port}/admin")
    print("="*50 + "\n")
    app.run(debug=debug, host='0.0.0.0', port=port)

