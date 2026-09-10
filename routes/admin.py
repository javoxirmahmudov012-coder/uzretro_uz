from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models.user import AdminUser
from models.order import Order
from extensions import db
from datetime import datetime, timedelta
from sqlalchemy import func

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = AdminUser.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('✅ Xush kelibsiz!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('❌ Login yoki parol noto\'g\'ri!', 'danger')
    
    return render_template('admin/login.html')

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Tizimdan chiqildi.', 'info')
    return redirect(url_for('admin.login'))

@admin.route('/')
@admin.route('/dashboard')
@login_required
def dashboard():
    today = datetime.utcnow().date()
    week_ago = datetime.utcnow() - timedelta(days=7)
    
    stats = {
        'total': Order.query.count(),
        'new': Order.query.filter_by(status='new').count(),
        'processing': Order.query.filter_by(status='processing').count(),
        'ready': Order.query.filter_by(status='ready').count(),
        'today': Order.query.filter(
            func.date(Order.created_at) == today
        ).count(),
        'this_week': Order.query.filter(
            Order.created_at >= week_ago
        ).count(),
    }
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', stats=stats, recent_orders=recent_orders)

@admin.route('/orders')
@login_required
def orders():
    status_filter = request.args.get('status', '')
    search = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    
    query = Order.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if search:
        query = query.filter(
            db.or_(
                Order.customer_name.ilike(f'%{search}%'),
                Order.customer_phone.ilike(f'%{search}%'),
            )
        )
    
    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/orders.html', orders=orders, 
                          status_filter=status_filter, search=search)

@admin.route('/orders/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)

@admin.route('/orders/<int:order_id>/update-status', methods=['POST'])
@login_required
def update_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    valid_statuses = ['new', 'accepted', 'processing', 'ready', 'delivered', 'cancelled']
    if new_status in valid_statuses:
        old_status = order.status
        order.status = new_status
        order.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Mijozga Telegram xabar yuborish (agar telefon raqami bo'lsa)
        if new_status == 'ready':
            try:
                from automation.telegram_bot import send_order_ready_notification
                send_order_ready_notification(order)
            except Exception as e:
                print(f"Xabar yuborishda xato: {e}")
        
        flash(f'✅ Buyurtma holati yangilandi: {old_status} → {new_status}', 'success')
    else:
        flash('❌ Noto\'g\'ri holat!', 'danger')
    
    return redirect(url_for('admin.order_detail', order_id=order_id))

@admin.route('/orders/<int:order_id>/set-price', methods=['POST'])
@login_required
def set_price(order_id):
    order = Order.query.get_or_404(order_id)
    price = request.form.get('price', type=float)
    is_paid = request.form.get('is_paid') == 'on'
    
    if price is not None:
        order.price = price
        order.is_paid = is_paid
        db.session.commit()
        flash('✅ Narx saqlandi!', 'success')
    
    return redirect(url_for('admin.order_detail', order_id=order_id))
