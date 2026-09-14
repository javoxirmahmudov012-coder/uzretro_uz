from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_from_directory, current_app
from models.order import Order
from extensions import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/services')
def services():
    return render_template('services.html')

@main.route('/pricing')
def pricing():
    return render_template('pricing.html')

@main.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        service = request.form.get('service', '')
        quantity = request.form.get('quantity', 1)
        description = request.form.get('description', '').strip()
        
        if not name or not phone or not service:
            flash('Iltimos, barcha majburiy maydonlarni to\'ldiring!', 'danger')
            return redirect(url_for('main.order'))
        
        new_order = Order(
            customer_name=name,
            customer_phone=phone,
            customer_email=email if email else None,
            customer_address=address if address else None,
            service_type=service,
            quantity=int(quantity) if quantity else 1,
            description=description if description else None,
        )
        db.session.add(new_order)
        db.session.commit()
        
        # Telegram xabar yuborish
        try:
            from automation.telegram_bot import send_new_order_notification
            send_new_order_notification(new_order)
        except Exception as e:
            print(f"Telegram xabar yuborishda xato: {e}")
        
        flash(f'✅ Buyurtmangiz qabul qilindi! Tez orada siz bilan bog\'lanamiz, {name}!', 'success')
        return redirect(url_for('main.order_success', order_id=new_order.id))
    
    return render_template('order.html')

@main.route('/order/success/<int:order_id>')
def order_success(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_success.html', order=order)

@main.route('/gallery')
def gallery():
    return render_template('gallery.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/api/order-status/<int:order_id>')
def order_status_api(order_id):
    order = Order.query.get_or_404(order_id)
    badge_text, badge_color = order.status_badge()
    return jsonify({
        'id': order.id,
        'status': order.status,
        'status_text': badge_text,
        'service': order.service_name(),
        'customer_name': order.customer_name,
        'created_at': order.created_at.strftime('%d.%m.%Y %H:%M'),
    })

@main.route('/robots.txt')
def robots():
    return send_from_directory(current_app.static_folder, 'robots.txt')

@main.route('/sitemap.xml')
def sitemap():
    return send_from_directory(current_app.static_folder, 'sitemap.xml', mimetype='application/xml')

@main.route('/google1453207274e1823c.html')
def google_verify():
    return send_from_directory(current_app.static_folder, 'google1453207274e1823c.html')
